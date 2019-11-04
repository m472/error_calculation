# coding: utf-8

import numpy as np
import math, re
from sympy import var, sin, sqrt, atan
from sympy.core.symbol import Symbol
from sympy.printing.latex import latex 

class MissingSubstitutionException(Exception):
    pass

def to_latex(expr):
    '''converts a sympy expression to a latex expression and substitutes certain variables (e.g. \phi to \varphi)'''
    return latex(expr, mul_symbol='dot').replace(r'\phi', r'\varphi')

def number_to_latex(number_str):
    '''
    converts the scientific notation of a number (e.g. 1.23e+02) to a nice latex expression (e.g. '1.23 \cdot 10^{2}')
    '''
    return re.sub(r'(.*)e\+?(\-?)0*(\d+)$', r'\1 \\cdot 10^{\2\3}', number_str)

def assert_numerical(expr):
    '''
    checks for forgotten substitutions and generates an error if any are found
    '''
    for atom in expr.atoms():
        if isinstance(atom, Symbol):
            raise MissingSubstitutionException(f"Numerical substitution for {atom} is missing. Please provide it in the substitutions dictionary.")

def calculate_error(expr, result_variable, substitutions, result_unit, blacklist):
    '''
    Calculates the error on a calculation by taking the partial derivative for every variable and multiplying
    it by the measuremnt uncertenty.
    
    The output is a latex string containing the error calculation both as an algebraic and a numerical expression.

    expr            -- sympy expression
    result_variable -- latex expression for the result
    substitutions   -- dictionay of values for variable substitutions. The keys can be either strings or sympy variables
    result_unit     -- string for the unit of the result (as a latex expression)
    blacklist       -- list of variables in expr that should not be taken into account for the error calculation
    '''
    
    latex_str_abst = '\sqrt{'
    latex_str = '\sqrt{'
    latex_str_num = '\sqrt{'
    num_result = 0

    first = True
    for atom in expr.atoms():
        if isinstance(atom, Symbol) and not atom in blacklist:
            d_var = var('Delta_{0}'.format(atom))
            
            if first:
                first = False
            else:
                latex_str_abst += '+'
                latex_str += '+'
                latex_str_num += '+'
                
            latex_str_abst += r'\left['
            latex_str_abst += r'\frac{\partial ' + result_variable +'}{\partial ' + to_latex(atom) + '}'
            latex_str_abst += r'\right]^2'
            latex_str_abst += f'\cdot {to_latex(d_var)}'
                
            latex_str += r'\left['
            latex_str += to_latex((expr.diff(atom)))
            latex_str += r'\right]^2'
            latex_str += f'\cdot {to_latex(d_var)}'
            
            num = ((expr.diff(atom) * d_var)**2).subs(substitution_values)
            assert_numerical(num)
            latex_str_num += number_to_latex(f'{num:.3g}')
            latex_str_num += r'\,' + expr_unit_str + '^2'
            
            num_result += num
            
    latex_str_abst += '}'
    latex_str += '}'
    latex_str_num += '}'
    num_result = math.sqrt(num_result)
            
    return f'\Delta_{result_variable} = {latex_str_abst} = {latex_str} = {latex_str_num} = ' + number_to_latex(f'{num_result:.3g}') + '\,' + expr_unit_str


if __name__ == "__main__":
    # Example:
    
    # create variables
    g,l, m, h, b, d = var('g, l, m, h, b, d')
    E = var('E')

    expr = (4 * g * (l**3) * m)/(h * b* (d**3))
    blacklist = [m, g]

    substitution_values = { 
        l : 0.354,
        g : 9.8,
        h : 0.00158,
        b : 0.00598,
        d : 0.00796,
        m : 1,
        'Delta_l' : 0.001,
        'Delta_b' : 0.00001,
        'Delta_h' : 0.00002,
        'Delta_d' : 0.00001,
    }
    expr_unit_str = r'\mathrm{GPa}'

    print("Error calculation for:")
    print(to_latex(expr))
    print()

    print(calculate_error(expr, 'E', substitution_values, expr_unit_str, blacklist))