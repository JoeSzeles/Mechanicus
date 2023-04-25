#!/usr/bin/env python
#bezmisc.py
import math, cmath

def rootWrapper(a,b,c,d):
    if a:
        # Monics formula see http://en.wikipedia.org/wiki/Cubic_function#Monic_formula_of_roots
        a,b,c = (b/a, c/a, d/a)
        m = 2.0*a**3 - 9.0*a*b + 27.0*c
        k = a**2 - 3.0*b
        n = m**2 - 4.0*k**3
        w1 = -.5 + .5*cmath.sqrt(-3.0)
        w2 = -.5 - .5*cmath.sqrt(-3.0)
        if n < 0:
            m1 = pow(complex((m+cmath.sqrt(n))/2),1./3)
            n1 = pow(complex((m-cmath.sqrt(n))/2),1./3)
        else:
            if m+math.sqrt(n) < 0:
                m1 = -pow(-(m+math.sqrt(n))/2,1./3)
            else:
                m1 = pow((m+math.sqrt(n))/2,1./3)
            if m-math.sqrt(n) < 0:
                n1 = -pow(-(m-math.sqrt(n))/2,1./3)
            else:
                n1 = pow((m-math.sqrt(n))/2,1./3)
        x1 = -1./3 * (a + m1 + n1)
        x2 = -1./3 * (a + w1*m1 + w2*n1)
        x3 = -1./3 * (a + w2*m1 + w1*n1)
        return (x1,x2,x3)
    elif b:
        det=c**2.0-4.0*b*d
        if det:
            return (-c+cmath.sqrt(det))/(2.0*b),(-c-cmath.sqrt(det))/(2.0*b)
        else:
            return -c/(2.0*b),
    elif c:
        return 1.0*(-d/c),
    return ()

def bezierparameterize(b):
    bx0,by0 = b[0]
    bx1,by1 = b[1]
    bx2,by2 = b[2]
    bx3,by3 = b[3]

    #parametric bezier
    x0=bx0
    y0=by0
    cx=3*(bx1-x0)
    bx=3*(bx2-bx1)-cx
    ax=bx3-x0-cx-bx
    cy=3*(by1-y0)
    by=3*(by2-by1)-cy
    ay=by3-y0-cy-by

    return ax,ay,bx,by,cx,cy,x0,y0
    #ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))

def bezierparameterize(coords):
    ((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)) = coords
    #parametric line
    dd=lx1
    cc=lx2-lx1
    bb=ly1
    aa=ly2-ly1

    if aa:
        coef1=cc/aa
        coef2=1
    else:
        coef1=1
        coef2=aa/cc

    ax,ay,bx,by,cx,cy,x0,y0=bezierparameterize(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)))
    #cubic intersection coefficients
    a=coef1*ay-coef2*ax
    b=coef1*by-coef2*bx
    c=coef1*cy-coef2*cx
    d=coef1*(y0-bb)-coef2*(x0-dd)

    roots = rootWrapper(a,b,c,d)
    retval = []
    for i in roots:
        if type(i) is complex and i.imag==0:
            i = i.real
        if type(i) is not complex and 0<=i<=1:
            retval.append(bezierpointatt(((bx0,by0),(bx1,by1),(bx2,by2),(bx3,by3)),i))
    return retval

def bezierpointatt(bezier, t):
    bx0, by0 = bezier[0]
    bx1, by1 = bezier[1]
    bx2, by2 = bezier[2]
    bx3, by3 = bezier[3]

    x = (1-t)**3*bx0 + 3*t*(1-t)**2*bx1 + 3*t**2*(1-t)*bx2 + t**3*bx3
    y = (1-t)**3*by0 + 3*t*(1-t)**2*by1 + 3*t**2*(1-t)*by2 + t**3*by3

    return x, y
def beziertatslope(bezier, slope):
    bx0, by0 = bezier[0]
    bx1, by1 = bezier[1]
    bx2, by2 = bezier[2]
    bx3, by3 = bezier[3]

    if slope[1]:
        t = (slope[0]/slope[1] - by0 + 3*by1 - 3*by2 + by3)/(3*(by3 - 3*by2 + 3*by1 - by0))
    elif slope[0]:
        t = (slope[1]/slope[0] - bx0 + 3*bx1 - 3*bx2 + bx3)/(3*(bx3 - 3*bx2 + 3*bx1 - bx0))
    else:
        return []

    if t < 0 or t > 1:
        return []

    return t



    
def bezierslopeatt(p0,p1,p2,p3,t):
    a = (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t ** 2 + (2 * p0[0] - 4 * p1[0] + 2 * p2[0]) * t + (-p0[0] + p1[0])
    b = (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t ** 2 + (2 * p0[1] - 4 * p1[1] + 2 * p2[1]) * t + (-p0[1] + p1[1])
    return (a, b)

def bezierslopeatt(bezier, t):
    bx0, by0 = bezier[0]
    bx1, by1 = bezier[1]
    bx2, by2 = bezier[2]
    bx3, by3 = bezier[3]

    dx = 3*(1-t)**2*(bx1-bx0) + 6*(1-t)*t*(bx2-bx1) + 3*t**2*(bx3-bx2)
    dy = 3*(1-t)**2*(by1-by0) + 6*(1-t)*t*(by2-by1) + 3*t**2*(by3-by2)

    return dx, dy


def tpoint(p1,p2,t):
    x1, y1 = p1
    x2, y2 = p2
    x = (1-t)*x1 + t*x2
    y = (1-t)*y1 + t*y2
    return (x,y)
def beziersplitatt(bezier, t):
    bx0, by0 = bezier[0]
    bx1, by1 = bezier[1]
    bx2, by2 = bezier[2]
    bx3, by3 = bezier[3]

    m1 = ((1-t)*bx0 + t*bx1, (1-t)*by0 + t*by1)
    m2 = ((1-t)*bx1 + t*bx2, (1-t)*by1 + t*by2)
    m3 = ((1-t)*bx2 + t*bx3, (1-t)*by2 + t*by3)
    m4 = ((1-t)*m1[0] + t*m2[0], (1-t)*m1[1] + t*m2[1])
    m5 = ((1-t)*m2[0] + t*m3[0], (1-t)*m2[1] + t*m3[1])
    m6 = ((1-t)*m4[0] + t*m5[0], (1-t)*m4[1] + t*m5[1])

    left_curve = (bezier[0], m1, m4, m6)
    right_curve = (m6, m5, m3, bezier[3])

    return left_curve, right_curve



'''
Approximating the arc length of a bezier curve
according to <http://www.cit.gu.edu.au/~anthony/info/graphics/bezier.curves>

if:
    L1 = |P0 P1| +|P1 P2| +|P2 P3| 
    L0 = |P0 P3|
then: 
    L = 1/2*L0 + 1/2*L1
    ERR = L1-L0
ERR approaches 0 as the number of subdivisions (m) increases
    2^-4m

Reference:
Jens Gravesen <gravesen@mat.dth.dk>
"Adaptive subdivision and the length of Bezier curves"
mat-report no. 1992-10, Mathematical Institute, The Technical
University of Denmark. 
'''
def pointdistance(x1,y1,x2,y2):
    return math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
def Gravesen_addifclose(b, len, error = 0.001):
    box = 0
    for i in range(1,4):
        box += pointdistance(b[i-1], b[i])
    chord = pointdistance(b[0], b[3])
    if (box - chord) > error:
        first, second = beziersplitatt(b, 0.5)
        Gravesen_addifclose(first, len, error)
        Gravesen_addifclose(second, len, error)
    else:
        len[0] += (box / 2.0) + (chord / 2.0)
def bezierlengthGravesen(b, error = 0.001):
    len = [0]
    Gravesen_addifclose(b, len, error)
    return len[0]

# balf = Bezier Arc Length Function
balfax,balfbx,balfcx,balfay,balfby,balfcy = 0,0,0,0,0,0
def balf(t):
    retval = (balfax*(t**2) + balfbx*t + balfcx)**2 + (balfay*(t**2) + balfby*t + balfcy)**2
    return math.sqrt(retval)

def Simpson(f, a, b, n_limit, tolerance):
    n = 2
    multiplier = (b - a)/6.0
    endsum = f(a) + f(b)
    interval = (b - a)/2.0
    asum = 0.0
    bsum = f(a + interval)
    est1 = multiplier * (endsum + (2.0 * asum) + (4.0 * bsum))
    est0 = 2.0 * est1
    #print multiplier, endsum, interval, asum, bsum, est1, est0
    while n < n_limit and abs(est1 - est0) > tolerance:
        n *= 2
        multiplier /= 2.0
        interval /= 2.0
        asum += bsum
        bsum = 0.0
        est0 = est1
        for i in xrange(1, n, 2):
            bsum += f(a + (i * interval))
            est1 = multiplier * (endsum + (2.0 * asum) + (4.0 * bsum))
    #print multiplier, endsum, interval, asum, bsum, est1, est0
    return est1

def bezierlengthSimpson(bx0, by0, bx1, by1, bx2, by2, bx3, by3, tolerance=0.001):
    global balfax, balfbx, balfcx, balfay, balfby, balfcy
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(
        ((bx0, by0), (bx1, by1), (bx2, by2), (bx3, by3)))
    balfax, balfbx, balfcx, balfay, balfby, balfcy = 3 * ax, 2 * bx, cx, 3 * ay, 2 * by, cy
    return Simpson(balf, 0.0, 1.0, 4096, tolerance)


def beziertatlength(bezier, l=0.5, tolerance=0.001):
    global balfax, balfbx, balfcx, balfay, balfby, balfcy
    ax, ay, bx, by, cx, cy, x0, y0 = bezierparameterize(bezier)
    balfax, balfbx, balfcx, balfay, balfby, balfcy = 3*ax, 2*bx, cx, 3*ay, 2*by, cy
    t = 1.0
    tdiv = t
    curlen = Simpson(balf, 0.0, t, 4096, tolerance)
    targetlen = l * curlen
    diff = curlen - targetlen
    while abs(diff) > tolerance:
        tdiv /= 2.0
        if diff < 0:
            t += tdiv
        else:
            t -= tdiv            
        curlen = Simpson(balf, 0.0, t, 4096, tolerance)
        diff = curlen - targetlen
    return t


#default bezier length method
bezierlength = bezierlengthSimpson

if __name__ == '__main__':
#    import timing
    #print linebezierintersect(((,),(,)),((,),(,),(,),(,)))
    #print linebezierintersect(((0,1),(0,-1)),((-1,0),(-.5,0),(.5,0),(1,0)))
    tol = 0.00000001
    curves = [((0,0),(1,5),(4,5),(5,5)),
            ((0,0),(0,0),(5,0),(10,0)),
            ((0,0),(0,0),(5,1),(10,0)),
            ((-10,0),(0,0),(10,0),(10,10)),
            ((15,10),(0,0),(10,0),(-5,10))]
    '''
    for curve in curves:
        timing.start()
        g = bezierlengthGravesen(curve,tol)
        timing.finish()
        gt = timing.micro()

        timing.start()
        s = bezierlengthSimpson(curve,tol)
        timing.finish()
        st = timing.micro()

        print g, gt
        print s, st
    '''
    for curve in curves:
        print (beziertatlength(curve,0.5))


# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 encoding=utf-8 textwidth=99
