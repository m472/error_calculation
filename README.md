# error_calculation    

Calculates the error on a calculation by taking the partial derivative for every variable and multiplying
it by the measuremnt uncertenty.
    
The output is a latex string containing the error calculation both as an algebraic and a numerical expression.
# Example:
    
```python
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
```

Output:
```
Error calculation for:
\frac{4 \cdot g \cdot l^{3} \cdot m}{b \cdot d^{3} \cdot h}

\Delta_E = \sqrt{\left[\frac{\partial E}{\partial h}\right]^2\cdot \Delta_{h}+\left[\frac{\partial E}{\partial l}\right]^2\cdot \Delta_{l}+\left[\frac{\partial E}{\partial d}\right]^2\cdot \Delta_{d}+\left[\frac{\partial E}{\partial b}\right]^2\cdot \Delta_{b}} = \sqrt{\left[- \frac{4 \cdot g \cdot l^{3} \cdot m}{b \cdot d^{3} \cdot h^{2}}\right]^2\cdot \Delta_{h}+\left[\frac{12 \cdot g \cdot l^{2} \cdot m}{b \cdot d^{3} \cdot h}\right]^2\cdot \Delta_{l}+\left[- \frac{12 \cdot g \cdot l^{3} \cdot m}{b \cdot d^{4} \cdot h}\right]^2\cdot \Delta_{d}+\left[- \frac{4 \cdot g \cdot l^{3} \cdot m}{b^{2} \cdot d^{3} \cdot h}\right]^2\cdot \Delta_{b}} = \sqrt{2.13 \cdot 10^{19}\,\mathrm{GPa}^2+9.56 \cdot 10^{18}\,\mathrm{GPa}^2+1.89 \cdot 10^{18}\,\mathrm{GPa}^2+3.72 \cdot 10^{17}\,\mathrm{GPa}^2} = 5.76 \cdot 10^{9}\,\mathrm{GPa}
```
## Rendered output
Input expression:
![equation](https://latex.codecogs.com/png.latex?%5Cfrac%7B4%20%5Ccdot%20g%20%5Ccdot%20l%5E%7B3%7D%20%5Ccdot%20m%7D%7Bb%20%5Ccdot%20d%5E%7B3%7D%20%5Ccdot%20h%7D)

Error calculation:
![equation](https://latex.codecogs.com/png.latex?%5Cdpi%7B200%7D%20%5Ctiny%20%5CDelta_E%20%3D%20%5Csqrt%7B%5Cleft%5B%5Cfrac%7B%5Cpartial%20E%7D%7B%5Cpartial%20h%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bh%7D&plus;%5Cleft%5B%5Cfrac%7B%5Cpartial%20E%7D%7B%5Cpartial%20l%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bl%7D&plus;%5Cleft%5B%5Cfrac%7B%5Cpartial%20E%7D%7B%5Cpartial%20d%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bd%7D&plus;%5Cleft%5B%5Cfrac%7B%5Cpartial%20E%7D%7B%5Cpartial%20b%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bb%7D%7D%20%5C%5C%20%3D%20%5Csqrt%7B%5Cleft%5B-%20%5Cfrac%7B4%20%5Ccdot%20g%20%5Ccdot%20l%5E%7B3%7D%20%5Ccdot%20m%7D%7Bb%20%5Ccdot%20d%5E%7B3%7D%20%5Ccdot%20h%5E%7B2%7D%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bh%7D&plus;%5Cleft%5B%5Cfrac%7B12%20%5Ccdot%20g%20%5Ccdot%20l%5E%7B2%7D%20%5Ccdot%20m%7D%7Bb%20%5Ccdot%20d%5E%7B3%7D%20%5Ccdot%20h%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bl%7D&plus;%5Cleft%5B-%20%5Cfrac%7B12%20%5Ccdot%20g%20%5Ccdot%20l%5E%7B3%7D%20%5Ccdot%20m%7D%7Bb%20%5Ccdot%20d%5E%7B4%7D%20%5Ccdot%20h%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bd%7D&plus;%5Cleft%5B-%20%5Cfrac%7B4%20%5Ccdot%20g%20%5Ccdot%20l%5E%7B3%7D%20%5Ccdot%20m%7D%7Bb%5E%7B2%7D%20%5Ccdot%20d%5E%7B3%7D%20%5Ccdot%20h%7D%5Cright%5D%5E2%5Ccdot%20%5CDelta_%7Bb%7D%7D%20%5C%5C%20%3D%20%5Csqrt%7B2.13%20%5Ccdot%2010%5E%7B19%7D%5C%2C%5Cmathrm%7BGPa%7D%5E2&plus;9.56%20%5Ccdot%2010%5E%7B18%7D%5C%2C%5Cmathrm%7BGPa%7D%5E2&plus;1.89%20%5Ccdot%2010%5E%7B18%7D%5C%2C%5Cmathrm%7BGPa%7D%5E2&plus;3.72%20%5Ccdot%2010%5E%7B17%7D%5C%2C%5Cmathrm%7BGPa%7D%5E2%7D%20%3D%205.76%20%5Ccdot%2010%5E%7B9%7D%5C%2C%5Cmathrm%7BGPa%7D)
