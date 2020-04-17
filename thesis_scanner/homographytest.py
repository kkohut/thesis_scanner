from pylab import *
import numpy as np

def homography_x(a, b, c, g, h, x, y):
    return ((a*x + b*y + c)/(g*x + h*y + 1))

def homography_y(d, e, f, g, h, x, y):
    return ((d*x + e*y + f)/(g*x + h*y + 1))


'''
If you have a set of points (0,0), (0,1), (1,0) and (1,1)
Then the homography matrix for another EQUAL set of points is:
(0 1 0) (a b c)
(1 0 0) (d e f)
(0 0 1) (g h i)

According to this one dude:
    -> a and e control scale along the x and y axes
    -> b and d control shear along each axis (together with a and e influnce rotation)
    -> c and f control translation along each axis
    -> g and h control perspective distortion along each axis

Green and red is the reversed one
blue and orange is the homographed one
'''

a = 1.0   # fixed scale factor in X direction with scale Y unchanged
e = 1.0   # fixed scale factor in Y direction with scale X unchanged

b = 0.0  # scale factor in X direction proportional to Y distance from origin
d = 0.0  # scale factor in Y direction proportional to X distance from origin

c = 0.0   # origin translation in X direction
f = 0.0   # origin translation in Y direction

g = 0.0
h = 0.0

H = np.array([[a, b, c], [d, e, f], [g, h, 1]])
print("Homography Matrix for new set:\n", H)
Hinverse = np.linalg.inv(H)
print("Reverse homography for the new set:\n",Hinverse)

ai = Hinverse[0][0]
bi = Hinverse[0][1]
ci = Hinverse[0][2]
di = Hinverse[1][0]
ei = Hinverse[1][1]
fi = Hinverse[1][2]
gi = Hinverse[2][0]
hi = Hinverse[2][1]


###

x1 = 1
y1 = 1
x2 = 1
y2 = 2
x3 = 2
y3 = 1
x4 = 2
y4 = 2



# Calculate homography

new_x1 = homography_x(a, b, c, g, h, x1, y1)
new_y1 = homography_y(d, e, f, g, h, x1, y1)

new_x2 = homography_x(a, b, c, g, h, x2, y2)
new_y2 = homography_y(d, e, f, g, h, x2, y2)

new_x3 = homography_x(a, b, c, g, h, x3, y3)
new_y3 = homography_y(d, e, f, g, h, x3, y3)

new_x4 = homography_x(a, b, c, g, h, x4, y4)
new_y4 = homography_y(d, e, f, g, h, x4, y4)



# Reverse homography

x1_inv = homography_x(ai, bi, ci, gi, hi, new_x1, new_y1)
y1_inv = homography_y(di, ei, fi, gi, hi, new_x1, new_y1)

x2_inv = homography_x(ai, bi, ci, gi, hi, new_x2, new_y2)
y2_inv = homography_y(di, ei, fi, gi, hi, new_x2, new_y2)

x3_inv = homography_x(ai, bi, ci, gi, hi, new_x3, new_y3)
y3_inv = homography_y(di, ei, fi, gi, hi, new_x3, new_y3)

x4_inv = homography_x(ai, bi, ci, gi, hi, new_x4, new_y4)
y4_inv = homography_y(di, ei, fi, gi, hi, new_x4, new_y4)

print("\nReverse x1 and y1: ", x1_inv, " ", y1_inv)
print("Reverse x2 and y2: ", x2_inv, " ", y2_inv)
print("Reverse x3 and y3: ", x3_inv, " ", y3_inv)
print("Reverse x4 and y4: ", x4_inv, " ", y4_inv)


# Plot all that shit

figure_old_x = [x1, x2, x3, x4]
figure_old_y = [y1, y2, y3, y4]

figure_new_x = [new_x1, new_x2, new_x3, new_x4]
figure_new_y = [new_y1, new_y2, new_y3, new_y4]

figure_reverse_x = [x1_inv, x2_inv, x3_inv, x4_inv]
figure_reverse_y = [y1_inv, y2_inv, y3_inv, y4_inv]
    
color_old = ['black']
color_new = ['green']

# scatter(figure_old_x , figure_old_y, s = 20, marker = 'o', c = color_old)
scatter(figure_new_x, figure_new_y, s = 20, marker = 'o', c = color_new)
scatter(figure_reverse_x, figure_reverse_y, s = 20, marker = 'o', c = color_old)

# plot(figure_old_x, figure_old_y, figure_old_y, figure_old_x)
# plot(figure_new_x, figure_new_y, figure_new_y, figure_new_x)
# plot(figure_reverse_x, figure_reverse_y, figure_reverse_y, figure_reverse_x)

grid()
show()



