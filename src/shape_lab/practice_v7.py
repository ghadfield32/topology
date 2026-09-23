"""Inspectably small reference answers; exercises are separate learner notebooks."""
import numpy as np


def table_dimensions(x):
    """Rows are observations; columns are the selected fields, not labels by default."""
    a=np.asarray(x)
    if a.ndim!=2: raise ValueError('A two-dimensional table is required')
    return a.shape


def compactness(area,perimeter):
    """4*pi*A/P**2; length units must be consistent before using this formula."""
    a=np.asarray(area,float);p=np.asarray(perimeter,float)
    if a.shape!=p.shape or not np.isfinite(a).all() or not np.isfinite(p).all() or np.any(a<=0) or np.any(p<=0):
        raise ValueError('Matching positive finite areas and perimeters required')
    return 4*np.pi*a/p**2


def fit_scaler(x):
    """Population standard deviation (ddof=0); constant columns get scale one."""
    a=np.asarray(x,float)
    if a.ndim!=2 or not a.size or not np.isfinite(a).all():raise ValueError('Finite nonempty 2D data required')
    center=a.mean(axis=0);scale=a.std(axis=0)
    return center,np.where(scale==0,1.,scale)


def class_counts(labels):
    """Counts observed integer classes, without guessing their semantic names."""
    values,counts=np.unique(np.asarray(labels),return_counts=True)
    return {int(k):int(v) for k,v in zip(values,counts)}


def absolute_errors(y,prediction):
    """Absolute residuals retain the physical units of the target."""
    y=np.asarray(y,float);p=np.asarray(prediction,float)
    if y.ndim!=1 or p.shape!=y.shape or not y.size or not np.isfinite(y).all() or not np.isfinite(p).all():raise ValueError('Matching finite vectors required')
    return np.abs(y-p)


def interval_bounds(prediction,radius):
    """Closed symmetric intervals. Negative lower strength is not silently clipped."""
    p=np.asarray(prediction,float);r=float(radius)
    if p.ndim!=1 or not p.size or not np.isfinite(p).all() or np.isnan(r) or r<0:raise ValueError('Finite predictions and nonnegative radius required')
    return p-r,p+r


def empirical_coverage(y,lower,upper):
    """Fraction of this finite sample within the supplied closed bounds."""
    y=np.asarray(y,float);lo=np.asarray(lower,float);hi=np.asarray(upper,float)
    if y.ndim!=1 or lo.shape!=y.shape or hi.shape!=y.shape or not y.size or not np.isfinite(y).all() or np.isnan(lo).any() or np.isnan(hi).any() or np.any(lo>hi):raise ValueError('Matching ordered interval bounds required')
    return float(np.mean((lo<=y)&(y<=hi)))


def mean_baseline(training_y,n):
    """A constant prediction fitted only to training outcomes."""
    y=np.asarray(training_y,float)
    if y.ndim!=1 or not y.size or not np.isfinite(y).all() or not isinstance(n,int) or n<1:raise ValueError('Finite training outcomes and positive count required')
    return np.full(n,y.mean())


def shared_rows(left,right):
    """Sorted intersection of row identities, not underlying participant identities."""
    return sorted(set(left)&set(right))


def shared_units(left,right,units):
    """Underlying unit IDs may overlap even when row indices do not."""
    u=np.asarray(units)
    return sorted(set(u[left])&set(u[right]))


def partition_by_units(units,selected):
    """Put all rows of each selected unit together; does not prove independence."""
    mask=np.isin(np.asarray(units),list(selected))
    return np.flatnonzero(mask),np.flatnonzero(~mask)


def apply_scaler(x,center,scale):
    """Apply fixed training parameters. Never refit them on validation or test."""
    x=np.asarray(x,float);c=np.asarray(center,float);s=np.asarray(scale,float)
    if x.ndim!=2 or c.shape!=(x.shape[1],) or s.shape!=c.shape or np.any(s<=0) or not np.isfinite(x).all() or not np.isfinite(c).all() or not np.isfinite(s).all():raise ValueError('Matching finite data and positive scales required')
    return (x-c)/s


def oscillator_energy(z):
    """Nondimensional unit harmonic oscillator H=(q**2+p**2)/2."""
    z=np.asarray(z,float)
    if z.shape!=(2,) or not np.isfinite(z).all():raise ValueError('One finite (q,p) vector required')
    return float(z@z/2)


def symplectic_defect(matrix):
    """Frobenius norm of A.T J A - J for a canonical two-dimensional map."""
    a=np.asarray(matrix,float)
    if a.shape!=(2,2) or not np.isfinite(a).all():raise ValueError('A finite 2x2 map is required')
    j=np.array([[0.,1.],[-1.,0.]])
    return float(np.linalg.norm(a.T@j@a-j))


def sphere_newton_step(x):
    """One linearized correction for C(x)=x.x-1; not exact radial projection."""
    a=np.asarray(x,float)
    if a.ndim!=1 or not a.size or not np.isfinite(a).all() or a@a==0:raise ValueError('Nonzero finite vector required')
    return a-((a@a-1)/(2*(a@a)))*a


def gradient_inner_product(g1,g2):
    """A negative inner product indicates conflicting first-order objectives."""
    a=np.asarray(g1,float);b=np.asarray(g2,float)
    if a.ndim!=1 or a.shape!=b.shape or not a.size or not np.isfinite(a).all() or not np.isfinite(b).all():raise ValueError('Matching finite gradients required')
    return float(a@b)
