"""Thirty-one entry lessons with distinct exact checks; preserve the original stages."""
from pathlib import Path
import json,textwrap
R=Path(__file__).resolve().parents[1]
STAGES=json.loads((R/'docs/v6/stage_transfer.json').read_text())
E=[]
def add(n,question,vocabulary,explanation,code,bridge,trap,assignment,answer):
 E.append(dict(stage=n,question=question,vocabulary=vocabulary,explanation=explanation,code=textwrap.dedent(code).strip(),bridge=bridge,trap=trap,assignment=assignment,answer=answer))
add(0,'What is one observation, and how is it stored?',
'Observation: one recorded object or event. Feature: an input measurement. Target: an outcome or category. Array axis: one direction in an organized collection.',
'''Start with a single kernel. Seven feature values describe it; they are not seven separate kernels. Put 210 kernels underneath one another and you obtain a 210-by-7 feature table. The source file also contains a target and our generated row ID, so its full table has nine columns. Selecting the seven inputs is a scientific choice, not just slicing an array.

In Python, `table[features]` selects the named fields and `.shape` returns two integers. The first counts rows; the second counts selected fields. Printing the first five rows gives examples, not proof of all 210 rows. The loader also checks local file hashes and schema. It does not independently certify source transcription or biological validity. Numbers can be stored correctly and still be interpreted incorrectly.''',
'''from shape_lab.evidence_v7 import load_snapshot
from shape_lab.practice_v7 import table_dimensions
table, meta = load_snapshot('seeds')
assert table_dimensions(table[meta['features']]) == (210, 7)
assert table.shape == (210, 9)
print('210 observations; 7 selected features; 1 label and 1 source ID excluded.')''',
'Open the new Seeds case and the retained healthcare case. Both use extracted image measurements; neither bundles the original acquisition images. Explain that difference before discussing computer vision.',
'Running a notebook is not an independent answer. Write a prediction first and preserve it even when the code disproves it.',
'For 52 mixtures and seven ingredients, state the feature-array dimensions. Would three measured outputs count as three additional mixtures?',
'The input shape is (52,7). Three output columns describe each same mixture, so they do not increase the number of mixtures.')
add(1,'Why can the same matrix have different ranks?',
'Field: the rules for arithmetic. Rank: number of independent directions in a linear map. Kernel: inputs mapped to zero. Proof: an argument covering all stated cases.',
'''Over real numbers, the columns of [[1,1],[1,-1]] are independent: its determinant is -2. Over the two-element field, -1 equals 1, so the columns become identical and the rank is one. Arithmetic is part of the mathematical object, not a cosmetic implementation detail.

The course uses XOR elimination for homology over F2. Do not replace it with floating-point rank on a general binary matrix; real and mod-two dependence can differ. Here you can prove the result by solving the two equations. In F2, (1,1) is a nonzero kernel vector because 1+1=0. In the reals, only the zero vector is in this matrix's kernel. This hand calculation becomes important when boundaries are combined later.''',
'''import numpy as np
from shape_lab.algebra import rank_mod2
A=np.array([[1,1],[1,-1]])
assert np.linalg.matrix_rank(A)==2
assert rank_mod2(A)==1
assert np.all((A @ np.array([1,1])) % 2 == 0)
print('Rank over R: 2; rank over F2: 1.')''',
'Use two numerical columns from Seeds to practice matrix shape and centering, but do not interpret a label column as a continuous coordinate simply because it is numeric.',
'Verifying a few numerical examples is not a proof of the rank formula for every complex. Learn the reasoning and then use tests for implementation errors.',
'Over F2, what is 1+1, and what does it imply for adding an edge boundary to itself?',
'1+1=0. Adding the same boundary twice cancels it coefficient by coefficient. It does not remove a source observation from a dataset.')
add(2,'What must a distance function satisfy?',
'Metric: a nonnegative, symmetric distance separating distinct points and satisfying the triangle inequality. Neighborhood: nearby points defined by the chosen space.',
'''For points 0,1,2 on a line, ordinary distances are 1,1 and 2. Squaring them gives 1,1 and 4. The alleged direct distance 4 is now greater than 1+1, so squared distance violates the triangle inequality. A formula useful in an optimization loss is not automatically a metric.

A metric gives open balls. These give a topology: a way to specify neighborhoods and continuous maps. In a finite distinct point sample with Euclidean distance, each point can be isolated by a sufficiently small ball. That finite topology is discrete. TDA does not magically discover a continuous circle inside the finite topology; it constructs complexes using distances at larger scales. Keep the sample, metric, complex and inferred underlying object separate.''',
'''d=lambda x,y: abs(x-y)
sq=lambda x,y: (x-y)**2
assert d(0,2) <= d(0,1)+d(1,2)
assert sq(0,2) > sq(0,1)+sq(1,2)
print('Squared distance: 4 > 1 + 1, so it is not a metric on R.')''',
'Compare raw and standardized Seeds distances. Their neighborhoods answer different questions. Source area and length units are unresolved, so do not invent a physical metric.',
'A triangle-inequality check on one sample can falsify a metric claim, but passing a finite sample is not a universal proof.',
'Would multiplying every distance by a fixed positive constant preserve the metric axioms? Explain rather than sample.',
'Yes. Nonnegativity, symmetry and zero separation remain; multiplying both sides of every triangle inequality by the same positive constant preserves it.')
add(3,'Why is a continuous bijection not always a homeomorphism?',
'Preimage: inputs mapped into a set. Continuity: preimages of open sets are open. Homeomorphism: a bijection continuous in both directions.',
'''Take the same two points {0,1} with two topologies. The discrete topology declares every subset open. A coarser topology declares only the empty set, {1}, and the whole set open. The identity from the discrete space to the coarser space is continuous because each preimage is open in the discrete domain.

The inverse identity is not continuous: the set {0} is open in its codomain but not in its domain. No coordinates moved, yet the topological structures differ. This is why the inverse-continuity condition matters. The finite checker below exhausts this particular example; it is not a general automatic theorem prover for arbitrary spaces. Later compactness and Hausdorff assumptions give useful sufficient conditions for continuous bijections to be homeomorphisms.''',
'''empty=frozenset();whole=frozenset({0,1})
discrete={empty,frozenset({0}),frozenset({1}),whole}
coarse={empty,frozenset({1}),whole}
identity_continuous=lambda domain,codomain: all(U in domain for U in codomain)
assert identity_continuous(discrete,coarse)
assert not identity_continuous(coarse,discrete)
print('The identity is a continuous bijection in one direction, not a homeomorphism.')''',
'Projection of seven real measurement columns onto two plotted columns can discard information. A visually tidy scatterplot does not establish invertibility of that projection.',
'A plot may suggest a map but does not specify its domain, codomain or topologies. State those before checking continuity.',
'What extra condition on the inverse is required in the definition of homeomorphism?',
'The inverse must be continuous. Merely existing as a set-theoretic inverse is insufficient.')
add(4,'Can doing two valid symmetries in opposite orders change the result?',
'Group: a set of composable operations with identity, inverses and associativity. Noncommuting: operation order matters. Homotopy: a continuous deformation of maps.',
'''Rotate a square by a quarter turn, then reflect it across the horizontal axis. Compare reflecting first and rotating second. Each operation preserves the square, but their products differ. A group need not be commutative.

Matrix multiplication represents composition here: the rightmost matrix acts first on a column vector. This convention will matter again in camera transforms. Path concatenation leads to another group idea after passing to homotopy classes of loops. That does not mean ordinary concatenated paths have all group laws literally before equivalence classes are introduced. Draw the loops, explain the equivalence, and only then use the algebraic language.''',
'''import numpy as np
R=np.array([[0,-1],[1,0]])
F=np.diag([1,-1])
assert np.array_equal(R@R@R@R,np.eye(2))
assert not np.array_equal(R@F,F@R)
print('RF=',R@F,'FR=',F@R)''',
'Rotate a real handwritten-digit image in the existing stage lab. A symmetry of the pixel grid is not automatically a label-preserving symmetry of the classification task.',
'Do not assume every transformation you can perform should preserve a target label. The observation process and task matter.',
'If A maps camera 1 to camera 2 and B maps camera 2 to world coordinates, which product maps a camera-1 column vector to world?',
'B A, since A acts first. Consistent domain/codomain descriptions are stronger than guessing from variable names.')
add(5,'What changes when a triangular outline is filled?',
'Simplex: a vertex, edge, triangle or higher-dimensional analogue. Face: a lower-dimensional part. Complex: a compatible collection containing the faces it requires.',
'''Three pairwise edges form a triangular outline. Adding one triangular face fills it. The vertices and edges remain; the two-dimensional simplex is new. An abstract complex records which vertex subsets form simplices, not just a drawing.

A triangle requires all three edges and all three vertices. The closure function intentionally adds required faces when constructing a complex. The validator, by contrast, rejects an incomplete supplied complex. These functions have different contracts: silent repair during validation can hide an upstream bug. A graph alone is not interchangeable with the clique complex that fills its cliques.''',
'''from shape_lab.algebra import closure,validate_complex
outline=closure([(0,1),(1,2),(0,2)])
filled=closure([(0,1,2)])
assert len(outline)==6 and len(filled)==7
assert (0,1,2) not in outline and (0,1,2) in filled
try:validate_complex([(0,1,2)])
except ValueError:print('Missing faces rejected as expected.')
else:raise AssertionError('Validator accepted missing faces')''',
'For a binary digit image, decide whether a foreground pixel represents its center or a closed square. Diagonal contact changes connectivity under different conventions.',
'Pretty triangulation pictures are not enough: save the actual simplices and the coordinate or pixel convention.',
'How many nonempty faces, including itself, does a tetrahedron contain?',
'Four vertices + six edges + four triangles + one tetrahedron =15. Its boundary excludes the final tetrahedron.')
add(6,'Why are cycles not automatically nontrivial holes?',
'Chain: a weighted combination of simplices. Cycle: a chain with zero boundary. Boundary: the boundary of a higher-dimensional chain. Homology: cycles modulo boundaries.',
'''A loop around a triangle has zero boundary because each endpoint cancels over F2. If the triangular face is absent, that loop is not the boundary of a two-chain in the complex. If the face is present, the same loop is its boundary. Homology identifies such boundaries with zero.

For finite complexes over a field, beta_k = number of k-simplices - rank(d_k) - rank(d_{k+1}). The boundary-of-boundary identity ensures the image of d_{k+1} lies inside the kernel of d_k, so the quotient makes sense. This is not a count of every visibly closed walk: many walks represent the same class or represent zero.''',
'''import numpy as np
from shape_lab.algebra import closure,boundary_matrix,betti_numbers
outline=closure([(0,1),(1,2),(0,2)]);filled=closure([(0,1,2)])
assert betti_numbers(outline,1)==[1,1]
assert betti_numbers(filled,1)==[1,0]
assert np.all((boundary_matrix(filled,1)@boundary_matrix(filled,2))%2==0)
print('Outline beta=[1,1]; filled beta=[1,0]; boundary of boundary is zero.')''',
'Threshold a real digit image in the retained lab. Its homology describes the chosen image complex, not a universal property of every handwritten instance of the class.',
'Homology depends on the space and coefficient system you selected. Equal Betti numbers do not generally prove two spaces homeomorphic.',
'Why must triangles be included when computing Rips H1 even if you only want one-dimensional output?',
'Two-simplices can make one-cycles into boundaries and kill H1 classes. Output dimension and construction dimension are different requirements.')
add(7,'Do pairwise intersections guarantee a common intersection?',
'Filtration: nested spaces indexed by a parameter. Rips complex: all vertex sets whose pairwise distances satisfy the threshold. Čech complex: common intersections of balls.',
'''Place three centers at the corners of an equilateral triangle with side length one. Balls of radius one half touch pairwise. Yet there is no point shared by all three: the circumradius is 1/sqrt(3), approximately .577, which exceeds .5. Pairwise proximity and common intersection encode different conditions.

For Rips with edge threshold one, the triangle enters because all three edges exist. For a Čech construction using radius-.5 balls, the corresponding face does not. The parameter units and factor-of-two conventions must be stated before comparing the two. GUDHI alpha filtrations additionally use a squared-radius convention by default; matching raw numeric thresholds across constructions would be misleading.''',
'''import numpy as np
side=1.;radius=.5;circumradius=side/np.sqrt(3)
assert 2*radius>=side
assert radius<circumradius
print('Pairwise touching radius:',radius,'common-intersection threshold:',circumradius)''',
'Build a Rips filtration on a small, declared subset of standardized Seeds or Wine measurements. Their mixed feature geometry is not a measured spatial reconstruction.',
'Increasing a proximity threshold eventually connects everything; connectivity at one large scale alone is not a discovery.',
'Why must an alpha filtration value of 4 not automatically be read as radius 4?',
'Under squared-radius convention it represents radius 2 in the same underlying coordinate units. Check the library’s exact convention.')
add(8,'When is a loop born, and what kills it?',
'Birth/death: parameter values where a class appears and disappears. Barcode: intervals of persistence. Essential/truncated: surviving the supplied filtration, possibly not an infinite extension.',
'''Four unit-square corners have side distances one and diagonal distances sqrt(2). At threshold one the perimeter edges form a loop and no triangular face is available. At sqrt(2), diagonals and the clique simplices enter and fill it. The positive H1 interval is [1,sqrt(2)).

Below one there are four components. Three H0 classes die when the perimeter becomes connected. Which vertex is selected as representative under equal-time ties is not a new scientific feature. The persistence maps matter, not only the Betti count at each separate scale. A finite computation ending before sqrt(2) would leave the loop with an unobserved death, not prove that it lives forever.''',
'''import numpy as np
from shape_lab.persistence import rips_filtration,persistent_homology,diagram
X=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
D=diagram(persistent_homology(rips_filtration(X,max_homology=1)),1,finite_only=True)
assert D.shape==(1,2) and np.allclose(D[0],[1,np.sqrt(2)])
print('Finite H1 interval:',D[0])''',
'Return to the CO2 delay-coordinate lab only after learning time windows. Filtration scale and chronological time are not the same axis.',
'A long bar is not a label such as “healthy,” “causal,” or “physically accurate.” Such interpretation needs independent evidence.',
'If all square coordinates are multiplied by three, what is the H1 interval under the same Euclidean edge convention?',
'[3,3sqrt(2)). Pairwise distances all scale by three; the coordinate transformation preserves topology but changes persistence coordinates.')
add(9,'What is a reduction algorithm actually checking?',
'Boundary column: encoded boundary of one simplex. Pivot: largest nonzero row in a reduced column. XOR: addition over F2. Pairing: birth/death relation from reduction.',
'''Take two vertices born at zero and their connecting edge born at one. Initially there are two components; after the edge, one remains. The boundary column of the edge has two nonzero vertex rows. Its pivot pairs one vertex class with that edge. One H0 interval is [0,1); another persists in the supplied filtration.

For larger examples, adding a previous column with the same pivot cancels that pivot. Repeat until the column is zero or has a new pivot. Store the operation trace so you can follow the algorithm rather than trust a barcode drawing. Faces must appear no later than cofaces; ties are ordered compatibly. Verify exact examples and boundary identities before benchmarking runtime.''',
'''import numpy as np
from shape_lab.persistence import persistent_homology,reduce_boundary
F=[((0,),0.),((1,),0.),((0,1),1.)]
bars=persistent_homology(F,max_dim=0)
assert len(bars)==2
assert sorted(b.death for b in bars)==[1.,np.inf]
f,columns,pairs,trace=reduce_boundary(F)
assert len(pairs)==1
print('Finite component death at 1; one surviving component. Pairs:',pairs)''',
'The manufacturing Stackloss case has few observations. That makes intermediate arrays inspectable but does not excuse fitting and reporting on the same rows.',
'Two libraries can share assumptions or conventions. Agreement helps, but independent hand calculations remain necessary; missing optional checks remain missing.',
'What must you record when one implementation includes zero-length bars and another omits them?',
'The policy and tie convention, then compare equivalent positive-length outputs or intentionally align the policies. Do not count the display difference as physical disagreement.')
add(10,'What does stability protect, and what does it not protect?',
'Bottleneck distance: smallest worst matching cost, allowing matches to the diagonal. Stability: bounded output change for a specified input perturbation. Significance: a statistical question.',
'''A finite persistence point (1,3) has lifetime two. Matching it to the diagonal costs half its lifetime, one, in the infinity norm. Comparing that diagram with an empty one therefore costs one. Moving it to (1.1,3.1) costs .1 if matched to its counterpart, which is better than deleting both.

This calculation is a distance between descriptors, not a probability that the underlying object is real. Stability theorems have hypotheses about functions, spaces and perturbation norms. Arbitrary preprocessing or a changed sensor can violate the comparison setting. In practice ask three questions separately: did the algorithm execute correctly, is its result stable to the perturbation of interest, and does it support the scientific interpretation?''',
'''import numpy as np
from shape_lab.persistence import finite_bottleneck
A=np.array([[1.,3.]])
assert np.isclose(finite_bottleneck(A,np.empty((0,2))),1.)
assert np.isclose(finite_bottleneck(A,A+.1),.1)
print('Deletion cost 1.0; matched shift cost 0.1.')''',
'Use the new Concrete Slump case to distinguish empirical prediction coverage from deterministic stability. These are different promises with different assumptions.',
'A stable error can remain wrong. A well-calibrated interval can be too wide to be useful. Measure the property you actually need.',
'What is the diagonal cost for an interval [2,8), and why?',
'Three: the diagonal midpoint is (5,5), with max(|2-5|,|8-5|)=3. Half the lifetime minimizes the infinity-norm distance.')
add(11,'How does an unfamiliar dataset become a model input?',
'Representation: a chosen numerical summary. Training: fitting model parameters. Validation: selecting or checking a procedure. Test: evaluating a fixed procedure on held-out units.',
'''A persistence diagram is a variable-sized collection. Many predictive models expect a fixed-length vector. A representation maps the diagram into features, such as counts or sampled landscapes. That mapping may lose information and may have fitted parameters. It belongs inside the evaluation protocol.

For a simpler exact check, standardize training values [0,2]. Their mean is one and population standard deviation is one. A future value 100 transforms to 99. Refitting the mean with that future value would change the coordinate system using held-out information. A large transformed value is a signal to examine distribution shift, not a reason to secretly recenter the test set.''',
'''import numpy as np
from shape_lab.practice_v7 import fit_scaler,apply_scaler
center,scale=fit_scaler([[0.],[2.]])
assert np.allclose(apply_scaler([[100.]],center,scale),[[99.]])
print('Training mean 1, scale 1; future value becomes 99.')''',
'The retained Wine case compares ordinary, topological and combined features on matched rows. The new Seeds case intentionally keeps descriptive PH separate from classification.',
'Do not give one model more training observations or test-driven tuning and attribute the difference to its architecture.',
'Why is fitting a persistence-image grid using all test diagrams part of evaluation design rather than a harmless plotting step?',
'When that grid feeds a model, it is representation fitting influenced by held-out inputs. An inductive design fixes it from training data or an externally specified rule.')
add(12,'What does completing a capstone require?',
'Protocol: declared question and procedure. Baseline: a simpler comparison. Provenance: origin and transformations of evidence. Holdout: observations reserved for evaluation.',
'''A capstone is an argument supported by an executable analysis. Begin with a prediction-time question and an observation unit. Specify features, labels, metric, filtration, coefficient field, splitting rule, parameter choices and computational limits. Then compare a simple baseline with the proposed method on equivalent information.

Two rows can be different indices while sharing the same person or physical object. In the exact four-row example below, rows [0,2] and [1,3] are disjoint but both contain kernels A and B. The split is invalid for a new-kernel evaluation. A report that only checks row disjointness has missed the scientific unit. Your capstone should include counterexamples to its own likely failure modes.''',
'''from shape_lab.evidence_v7 import overlap_report
report=overlap_report({'train':[0,2],'test':[1,3]},['A','A','B','B'])
assert report['row_disjoint'] and not report['unit_disjoint']
print(report)''',
'Choose one of ten included industry cases as practice, then a genuinely new dataset or question for independent assessment. Repeatedly revisiting the supplied test labels is not a new holdout.',
'An empty “notebook ran” checklist does not defend a scientific conclusion. Keep explanations, predictions, wrong turns and exact output evidence.',
'Name five items another learner needs to reproduce your experiment.',
'Examples: source/version/hash, feature/target definitions and units, exact split identities, fitted preprocessing and model parameters, random seeds/environment, metric/filtration conventions, code and saved predictions.')
add(13,'How can two coordinate systems describe the same point?',
'Manifold: a space locally described by Euclidean coordinates under specified regularity. Chart: a local coordinate map. Transition: one chart followed by another chart inverse. Tangent: a local direction.',
'''Latitude-longitude intuition is useful, but start with a sphere and an explicit formula. A stereographic inverse sends planar coordinates (u,v) to (2u,2v,u²+v²-1)/(1+u²+v²). At (u,v)=(0,0), it gives the south pole. The missing north pole explains why this one chart does not cover the whole sphere.

Substituting the resulting coordinates into u=x/(1-z), v=y/(1-z) returns the same local coordinates. The round trip tests one representation pair. A chart is not a photograph of an arbitrary 3D scene: perspective projection loses depth along a ray. Smooth coordinate transitions preserve the underlying point, not identical coordinate numbers.''',
'''import numpy as np
u,v=.3,-.4;r2=u*u+v*v
p=np.array([2*u,2*v,r2-1])/(1+r2)
assert np.isclose(p@p,1.)
assert np.allclose(p[:2]/(1-p[2]),[u,v])
print('Sphere point:',p,'round trip:',p[:2]/(1-p[2]))''',
'The retained stage maps directions derived from real stereo references onto a constructed sphere. That construction is not evidence that the original scene is a sphere.',
'Local invertibility should not be upgraded to global invertibility. Always state the excluded set and chart domain.',
'Why does this inverse chart fail to recover finite (u,v) at the north pole?',
'The denominator 1-z is zero at z=1. The north pole is outside this chart and needs another patch.')
add(14,'How do you know a matrix is a valid rotation?',
'SO(3): orthogonal 3x3 matrices with determinant +1. Rigid transform: rotation plus translation. Frame: coordinate reference. Intrinsics: pixel projection parameters.',
'''A rotation preserves lengths and orientation: R^T R=I and det(R)=1. Nine arbitrary numbers do not generally satisfy these equations. A rigid transform then maps a point p to Rp+t. Its inverse is R^T(p-t), not R^T p-t unless a special coincidence holds.

For a quarter turn around the z-axis and translation (1,2,3), point (1,0,0) becomes (1,3,3). Applying the inverse returns (1,0,0). These are constructed coordinates with a declared common unit, not measured metre accuracy. A camera projection adds another mapping and discards information; testing transform inverses cannot by itself validate calibration.''',
'''import numpy as np
R=np.array([[0.,-1,0],[1,0,0],[0,0,1]])
t=np.array([1.,2.,3.]);p=np.array([1.,0.,0.]);q=R@p+t
assert np.allclose(R.T@R,np.eye(3)) and np.isclose(np.linalg.det(R),1.)
assert np.allclose(q,[1,3,3]) and np.allclose(R.T@(q-t),p)
print('Forward:',q,'inverse:',R.T@(q-t))''',
'Use calibrated stereo observations for physical reconstruction, not the Nile series or arbitrary tabular coordinates. The general lesson of units transfers; the camera model does not.',
'A matrix with determinant one alone is not necessarily a rotation in three dimensions. Orthogonality must also be checked.',
'What additional check rejects a shear matrix with determinant one as a rotation?',
'R^T R=I. A nontrivial shear changes lengths and angles and fails this orthogonality condition.')
add(15,'Why can a small disparity error produce a large depth error?',
'Disparity: horizontal correspondence difference under a rectified convention. Baseline: camera separation. Principal point: intrinsic reference pixel. Sensitivity: derivative of output to input.',
'''Under the retained stereo convention, Z=fB/(d+delta_cx). Let f=1000 pixels, B=.1 metres, d=20 pixels and delta_cx=5 pixels. Depth is 100/25=4 metres. Omitting the offset would give five metres, a 25% error in this constructed example.

Differentiating gives dZ/dd=-fB/(d+delta_cx)². At our values it is -.16 metres per pixel. This is a local sensitivity, not a universal constant or a complete uncertainty budget. Calibration, synchronization, rectification, occlusion and correspondence failures can all contribute. Validate the forward model and actual measured conventions before propagating a single noise term.''',
'''import numpy as np
f,B,d,offset=1000.,.1,20.,5.
Z=lambda disparity: f*B/(disparity+offset)
sensitivity=-f*B/(d+offset)**2
h=1e-4;finite_difference=(Z(d+h)-Z(d-h))/(2*h)
assert np.isclose(Z(d),4.) and np.isclose(sensitivity,-.16)
assert np.isclose(sensitivity,finite_difference)
print('Depth:',Z(d),'local metres/pixel:',sensitivity)''',
'The Middlebury case contains observed stereo images and supplied reference disparity. Its convention is documented. Manufactured perturbations are labeled as tests, not new measurements.',
'Low reprojection error alone can coexist with wrong scale or a weakly constrained configuration. Use independent measured holdouts.',
'What happens to depth sensitivity as a positive disparity denominator approaches zero?',
'Its magnitude grows without bound in this idealized formula. This exposes poor depth conditioning and does not justify reporting arbitrarily confident distant geometry.')
# The remaining entries are appended below.
add(16,'What does attention combine, and what has it not measured?',
'Token: an encoded input item. Query/key: vectors used to score relationships. Value: information to combine. Softmax: nonnegative weights summing to one.',
'''Attention scores compare a query with keys, then normalize those scores to weights. With equal scores, two values receive equal weights. Values (1,0) and (0,2) then produce (.5,1). This is a weighted combination, not a reconstructed physical coordinate merely because it has two entries.

VGGT uses learned image representations and alternating within-frame and across-frame information exchange. The original course explains its outputs and coordinate conventions. Our small attention calculation is an architectural teaching example, not trained VGGT inference. An output called depth still requires checking reference frame, scale, preprocessing and evidence before it can contribute to a metric world model.''',
'''import numpy as np
scores=np.array([0.,0.]);weights=np.exp(scores-scores.max());weights/=weights.sum()
values=np.array([[1.,0.],[0.,2.]])
output=weights@values
assert np.allclose(weights,[.5,.5]) and np.allclose(output,[.5,1.])
print('Weights:',weights,'weighted values:',output)''',
'The observed stereo pair can support a future model comparison, while tabular Seeds measurements can illustrate arrays only. The archive does not claim to have run VGGT weights.',
'Attention weights are not automatically probabilities of causal importance, physical visibility or trustworthy correspondence.',
'Why subtract the maximum score before exponentiating, and does it change softmax mathematically?',
'It improves numerical range. Multiplying every exponential by the same factor cancels in normalization, so exact-arithmetic softmax is unchanged.')
add(17,'What can registration fit, and where should you evaluate it?',
'Gauge: a representational ambiguity such as scale or frame. Registration: fitting a transform between representations. Holdout: separate references for evaluation.',
'''Suppose a model produces scalar coordinates x while measured references satisfy y=2x+3. Fit scale and translation on x=0,1,2, then evaluate x=3. The known construction gives the held-out prediction nine. A zero residual on the fitting points alone would not test transfer to a separate reference.

This is deliberately a one-dimensional affine example, not a full SE(3) or similarity-registration solver. The retained stage develops 3D registration and degenerate configurations. A fitted alignment can remove gauge differences but cannot repair every local deformation, missing surface or incorrect correspondence. Compare errors on references not used in fitting and report completeness alongside error.''',
'''import numpy as np
x=np.array([0.,1.,2.]);y=2*x+3
A=np.column_stack([x,np.ones(len(x))]);scale,offset=np.linalg.lstsq(A,y,rcond=None)[0]
prediction=scale*3+offset
assert np.allclose([scale,offset],[2,3]) and np.isclose(prediction,9.)
print('Fitted scale/offset:',scale,offset,'held-out prediction:',prediction)''',
'In the stereo experiment, distinguish reference points used to align coordinates from independent measured holdouts. In tabular cases, an analogous separation applies to fitting preprocessing and evaluating it.',
'Do not name an aligned reconstruction “ground truth.” Registration is a fitted operation with assumptions and residual errors.',
'Why can adding more fit points lower training error yet fail to establish held-out physical accuracy?',
'Fit error evaluates points used to choose parameters. It may hide overfitting, inappropriate transforms, degeneracy or systematic correspondence errors; separate holdouts test a different claim.')
add(18,'How can high throughput coexist with stale results?',
'Throughput: completed items per unit time. Latency: elapsed time for an item. Queue age: time since its arrival. p95: a percentile, not an average.',
'''If frames arrive every .033 seconds and a serial processor needs .06 seconds per frame, work accumulates. The first frame finishes at .06; the next arrives at .033 but cannot start until .06, finishing at .12. Its age is .087. The processor may be busy at constant throughput while the displayed result gets older.

The code below is a deterministic queue simulation, not a timing measurement of ROS2, a GPU, VGGT or your computer. Actual profiling must record arrival, queue, decode, preprocessing, device transfer, inference, postprocessing and display boundaries. Optimizing one kernel does not establish end-to-end improvement if copies or queues dominate.''',
'''import numpy as np
arrivals=np.arange(8)*.033;finish=0.;ages=[]
for arrival in arrivals:
    finish=max(finish,float(arrival))+.06
    ages.append(finish-arrival)
assert ages[-1]>ages[0]
print('Simulated result ages (seconds):',ages)''',
'The CO2 case illustrates time-index integrity, not video-frame performance. The retained pipeline lab measures CPU transformations separately from simulated queue behavior.',
'Do not turn a single matrix-multiplication timing into deterministic petascale throughput or live capture-to-overlay latency.',
'What two timestamps are needed to measure an individual result’s age at display?',
'The originating observation’s capture/arrival timestamp under a specified clock convention and the actual display timestamp. Queue and clock assumptions must be explicit.')
add(19,'When does a live detector actually know an event occurred?',
'Onset: candidate beginning. Confirmation: when sufficient evidence has arrived. Visibility: whether the required observation is available. Causal processing: uses past/present only.',
'''Assume a toy detector requires three consecutive visible distances below .1. Observed distances [.2,.08,.07,.06] begin satisfying the condition at index one, but confirmation is unavailable until index three. With .02-second spacing, confirmation follows candidate onset by .04 seconds.

Recording index one as onset is compatible with an online detector only if the output also records that it was emitted at index three. Otherwise a hindsight label is disguised as a zero-latency live decision. Proximity alone does not prove contact, controlled possession or release. Occlusion and tracking identities must remain part of the evidence.''',
'''distances=[.2,.08,.07,.06];dt=.02
run=0;confirmed=None;onset=None
for i,d in enumerate(distances):
    run=run+1 if d<.1 else 0
    if run==3:
        confirmed=i;onset=i-2;break
assert onset==1 and confirmed==3
assert abs((confirmed-onset)*dt-.04)<1e-12
print('Candidate onset:',onset,'confirmation:',confirmed,'delay:',.04)''',
'The retained temporal labs use manufactured controls and historical time series. Real basketball contact labels and synchronized observations are an independent-data obligation, not supplied by this toy signal.',
'A filled-in or smoothed track must not be relabeled as direct observation. Separate observed, interpolated and inferred evidence.',
'How should a missing required observation affect a three-consecutive-visible-samples rule?',
'Under that explicit rule it breaks the visible run. A different missing-data policy must be declared and validated, not silently substituted.')
add(20,'What does a file hash prove?',
'Hash: a content fingerprint. Reproducibility: ability to repeat a specified procedure. Validation: testing the appropriateness and accuracy of a claim. Provenance: evidence origin.',
'''A SHA-256 hash changes when a file’s bytes change. It can show that your reference output or source snapshot has not changed since the recorded fingerprint. It cannot establish that the file was scientifically correct, honestly collected or appropriate to the deployment question.

A spatial capstone needs both provenance and measurement evidence. Record camera conventions, input/weight revisions, calibration references, independent holdouts, visibility rules, uncertainty and timing. A checksum plus a successful script run is not a validated reconstruction. The supplied package keeps previous verification reports as dated historical records and current checks in the v7 report directory.''',
'''import hashlib
first=b'prediction=4.0\\n';changed=b'prediction=5.0\\n'
a=hashlib.sha256(first).hexdigest();b=hashlib.sha256(changed).hexdigest()
assert a!=b and a==hashlib.sha256(first).hexdigest()
print('Unchanged bytes match; changed bytes differ. Correctness is a separate question.')''',
'The new UCI snapshots have local hashes and canonical numeric fingerprints. They were transcribed from official retrieved text; they are not claimed as provider-byte-identical downloads.',
'A local checksum is not independent source verification. Nor does an unchanged wrong answer become right.',
'What evidence would turn a candidate scene reconstruction into a defensible metric result?',
'Explicit coordinate/scale conventions, known calibration, independently measured held-out references, quantified errors/completeness and uncertainties, documented failure modes and reproducible input/model provenance.')
add(21,'What does the derivative’s unit tell you?',
'Rate: change per change in an independent variable. ODE: derivatives in one independent variable. PDE: derivatives in several. Identifiability: whether distinct parameters can be distinguished by evidence.',
'''For x(t)=t², a central difference at t=2 with step h computes ((2+h)²-(2-h)²)/(2h)=4 exactly in algebra. The two h² terms cancel. This example demonstrates the formula; most functions have truncation error and floating-point effects.

If x is measured in metres and t in seconds, dx/dt has metres per second. The manufactured function here is nondimensional unless units are assigned consistently. Real mixture ingredients and response strength have different units; differentiating a fitted response with respect to an ingredient does not automatically identify its causal effect. Distinguish a descriptive function, an ODE state trajectory, and a table of independent observations.''',
'''import numpy as np
t=2.;h=1e-3
estimate=((t+h)**2-(t-h)**2)/(2*h)
assert np.isclose(estimate,4.)
print('Central difference for t² at t=2:',estimate)''',
'Concrete Slump supports mixture-response modeling. Nile supports a historical scalar sequence. Neither is automatically a full spatial field for solving an arbitrary PDE.',
'More precise arithmetic cannot resolve parameters that the observations do not identify. Check which variables were actually measured.',
'If time is converted from seconds to milliseconds, does the numerical velocity stay the same?',
'No. A numerical change per millisecond is one thousandth of the numerical change per second for the same physical motion, with the corresponding unit conversion.')
add(22,'Is a smooth local flow always defined for every time?',
'Flow: state evolution generated by a vector field. Diffeomorphism: smooth invertible map with smooth inverse. Local existence: valid only on an appropriate state/time domain.',
'''The scalar equation x_dot=x² has solution phi_t(x)=x/(1-tx) while the denominator stays away from zero along the solution. Starting at x=.5, the positive trajectory blows up at t=2. A local invertible flow does not imply global existence for arbitrary t.

Within the valid domain, composing phi_t with phi_-t returns the initial state. An explicit Euler update is a different map. For x_dot=-x and step h=1, Euler sends every x to zero; that discrete step is not invertible, even though the exact finite-time flow x exp(-t) is. Distinguish the vector field, its exact flow and an approximation.''',
'''import numpy as np
phi=lambda x,t:x/(1-t*x)
x=.5;t=.2;y=phi(x,t)
assert np.isclose(phi(y,-t),x)
assert np.isclose(1-2*x,0.)
assert (1-1.)*3. == (1-1.)*7. == 0.
print('Valid round trip:',x,y,phi(y,-t),'blow-up time:',2.)''',
'The retained smooth-flow stage connects to time-series windows and explicit coupling maps. It does not infer a governing vector field solely from an attractive delay-coordinate loop.',
'Invertibility of a neural architecture does not imply it models the correct physical dynamics or observed likelihood.',
'Why must the domain accompany the formula x/(1-tx)?',
'The denominator can vanish and a solution can leave its existence interval. The algebraic expression alone hides those conditions.')
add(23,'When are momentum and velocity different numbers?',
'Lagrangian: a function of position and velocity. Momentum: derivative of L with respect to velocity. Hamiltonian: the Legendre-transformed function when the transformation is regular.',
'''For L(q,v)=m v²/2-k q²/2 with positive mass, momentum is p=m v. When m=2 and v=.4, p=.8, not .4. The Hamiltonian computed as pv-L is m v²/2+k q²/2. For q=.3 and k=3 it is .295.

Recovering v from p requires an invertible relation. In more general learned Lagrangians, the velocity Hessian may be singular or ill-conditioned. A constrained or dissipative system may require additional structure. The retained small LNN example is explicitly restricted; it is not a full reproduction of every general Lagrangian architecture.''',
'''import numpy as np
m,k,q,v=2.,3.,.3,.4
p=m*v;L=.5*m*v*v-.5*k*q*q;H=p*v-L
assert np.isclose(p,.8) and np.isclose(H,.295)
assert np.isclose(H,p*p/(2*m)+.5*k*q*q)
print('Momentum:',p,'Hamiltonian:',H)''',
'Manufactured oscillator trajectories make dynamics derivatives testable. Static Stackloss measurements are an analogy for regression, not evidence of an unmeasured mechanical Hamiltonian.',
'Automatic differentiation computes derivatives of the implemented function; it does not prove the learned function is the true physical energy.',
'What property of the map from velocity to momentum matters for an ordinary Legendre transform back to velocity?',
'Local invertibility/regularity, typically a nonsingular velocity Hessian. Singular constrained cases require additional treatment.')
add(24,'Does preserving symplectic structure preserve the exact energy value each step?',
'Symplectic: preserving the canonical two-form. Energy: the specified Hamiltonian value. Phase error: timing or angular error along a trajectory. Stability region: step/system conditions.',
'''For the unit oscillator, kick-drift symplectic Euler is A=[[1-h²,h],[-h,1]]. With h=.2 it preserves A^T J A=J, but at state (1,0) energy changes from .5 to .4808. Both statements can be true at once.

The source post made a stronger discrete-step energy claim. We preserve it as an attributed claim and supply this separate original counterexample. The useful long-time properties of particular symplectic methods have hypotheses; they do not imply exact energy, exact phase or unconditional stability for arbitrary step sizes and learned models. The full stage compares several maps and reports those properties separately.''',
'''import numpy as np
from shape_lab.practice_v7 import symplectic_defect,oscillator_energy
h=.2;A=np.array([[1-h*h,h],[-h,1.]])
assert symplectic_defect(A)<1e-14
assert np.isclose(oscillator_energy(A@np.array([1.,0.])),.4808)
print('Symplectic condition passes; exact-energy condition does not.')''',
'The marine-climate series can motivate long-horizon evaluation, but this manufactured oscillator is not an atmospheric or ocean model. Do not transfer conservation claims without a governing model.',
'Volume preservation is not synonymous with symplecticity in every dimension; exact energy is another distinct property.',
'Why should an evaluation report both trajectory error and energy error?',
'A trajectory can remain near an energy level while accumulating phase or state error. Conversely, energy changes can be physically appropriate in a driven or dissipative system.')
add(25,'What problem does one projection step actually solve?',
'Constraint: an equation defining admissible states. Jacobian: local linear change. Retraction: a local manifold mapping with specified properties. Rank failure: loss of independent constraint information.',
'''For C(x)=x·x-1, linearize at (2,0). The residual is 3 and the Jacobian is (4,0). A minimum-norm correction solving the linearized equation subtracts (.75,0), leaving (1.25,0). Its original nonlinear constraint residual is .5625.

The step improved the residual without eliminating it. Iteration can help near a suitable solution; radial normalization happens to be exact for the sphere away from the origin. Neither method is an exact universal projection onto every nonlinear constraint set. At the origin, this Jacobian cannot determine the needed correction direction. Check rank, residual and physical meaning independently.''',
'''import numpy as np
from shape_lab.practice_v7 import sphere_newton_step
x=sphere_newton_step([2.,0.]);residual=x@x-1
assert np.allclose(x,[1.25,0.]) and np.isclose(residual,.5625)
print('One linearized correction:',x,'remaining residual:',residual)''',
'Transportation choice probabilities satisfy a sum constraint, but a sum-to-one vector is not automatically calibrated or causally meaningful. Constraint satisfaction is only one evaluation axis.',
'Enforcing one constraint can disturb another. A geometric projection need not preserve the integrator’s symplectic structure.',
'Why is solving the linearized constraint not the same as solving the nonlinear constraint?',
'The Taylor approximation omits higher-order terms. Those terms remain after a finite correction unless the constraint is affine or another special property applies.')
add(26,'Can a function satisfy a differential equation but violate its boundary conditions?',
'PINN: a network trained with differential-equation and other residuals. Collocation: locations where residuals are checked. Boundary condition: required behavior at the domain boundary.',
'''On [0,1], u=x(1-x) satisfies -u''=2 and u(0)=u(1)=0. Adding a constant five leaves the second derivative unchanged, so v=u+5 satisfies the same interior equation but violates both boundary values. Interior residual alone cannot identify the desired solution.

The lesson separates data, PDE, boundary and interface objectives. A small loss at sampled collocation points is not an exact theorem on an entire domain. Compare with an analytic or conventional numerical reference when one exists, and report held-out residuals and solution error. The retained Poisson PINN trains on a manufactured problem with a known solution; it is not a claim of industrial material-law recovery.''',
'''import numpy as np
u=lambda x:x*(1-x)
v=lambda x:u(x)+5
h=1e-3;x=.4
second=lambda f:(f(x+h)-2*f(x)+f(x-h))/h**2
assert np.isclose(-second(u),2.,atol=1e-6)
assert np.isclose(-second(v),2.,atol=1e-6)
assert u(0)==0 and v(0)==5
print('Same interior equation; different boundary values.')''',
'Concrete strength prediction is observed-data regression. Without a specified physical field, domain and equation, it is not transformed into a PINN merely by adding a regularization term.',
'Physics in the loss is not a guarantee that optimization found a physically valid or unique solution.',
'What extra information rules out u+5 in the worked boundary-value problem?',
'The zero boundary conditions. They distinguish the desired solution from constant-shift alternatives with the same second derivative.')
add(27,'Can an optimizer always decrease every objective at once?',
'Gradient conflict: objective gradients point in opposing directions. Domain decomposition: solving interacting subdomains. Interface condition: compatibility across subdomain boundaries.',
'''If g1=(1,0) and g2=(-1,0), an update -ηd decreases both objectives strictly to first order only when d1>0 and -d1>0. That is impossible. This exact local incompatibility cannot be removed by giving a gradient method a stronger name.

The supplied paper reports Norm-PCGrad improvements on its benchmarks and discusses PINN/PIKAN domain-decomposition failures. Preserve that empirical scope. Tests of small projection operations are not full benchmark replications. Wrong interface conditions, incorrect units or inconsistent boundary constraints must be corrected in the mathematical problem rather than hidden by changing loss weights.''',
'''import numpy as np
from shape_lab.practice_v7 import gradient_inner_product
g=np.array([1.,0.]);other=-g
assert gradient_inner_product(g,other)==-1.
for a in [-2.,-1.,0.,1.,2.]:
    assert not (a>0 and -a>0)
print('Opposite gradients admit no strictly common first-order descent direction.')''',
'Observed small manufacturing data can teach noisy objectives, but the supplied 2D/3D PDE benchmarks are not reproduced by a 21-row regression table.',
'Fewer operations for a separable mathematical form do not establish end-to-end hardware speedup at equal accuracy.',
'What evidence is needed to claim one gradient method outperforms another on a new PDE problem?',
'A specified PDE/domain/interface setup, matched model capacity/data/compute and tuning policy, held-out solution/residual metrics, repeated runs where appropriate, and reproduced timing rather than copied benchmark headlines.')
add(28,'How is learning an operator different from fitting one function?',
'Function: maps coordinates to values. Operator: maps functions to functions. Initial condition: a function specifying the starting field. Fourier mode: a sinusoidal basis component.',
'''For a periodic one-dimensional heat equation with diffusivity ν, an initial mode sin(kx) evolves as exp(-νk²t)sin(kx). Doubling k increases the decay exponent by four, not two. A neural operator attempts to learn a rule taking different input functions to their corresponding output functions.

Splitting spatial coordinates from one solution is not the same as testing unseen initial conditions. The retained DeepONet and Fourier-neural-operator labs use manufactured heat data with known solutions and function-level splits. Their small training results teach the machinery; they are not a universal ranking of architectures or evidence of multi-decadal climate accuracy.''',
'''import numpy as np
nu,t=.1,1.
a1=np.exp(-nu*t);a2=np.exp(-nu*4*t)
assert np.isclose(a2,a1**4)
print('Mode-1 amplitude:',a1,'mode-2 amplitude:',a2)''',
'The Well is an optional simulation-data extension with its own acquisition and license rules. The historical ocean-temperature series is observed but is not itself a full heat-equation field.',
'Interpolation at unseen grid points and generalization to unseen forcing functions are different tasks. Label the split unit.',
'What should be held out to test transfer to a new heat-equation initial profile?',
'Entire initial-condition functions and their solution trajectories, not merely coordinates sampled from profiles already used during fitting.')
add(29,'What exactly does differentiating through a simulator give you?',
'Sensitivity: derivative of output with respect to a parameter. Differentiable simulation: propagating derivatives through implemented operations. Identifiability: uniqueness supported by observations.',
'''For x(t)=exp(-ct), derivative with respect to damping c is -t exp(-ct). At c=.3,t=2 this is about -1.098. A central difference in c checks the implementation locally. The derivative concerns this specified model; it does not establish that the physical system actually obeys exponential decay.

Differentiating through a discrete solver returns sensitivities of that discretization. Tolerance, truncation, contact discontinuities and parameterization can matter. A successful gradient check is necessary evidence for many implementations, but it is not proof that an inverse problem is identifiable or that optimization found the intended parameters.''',
'''import numpy as np
c,t=.3,2.;h=1e-5
f=lambda value:np.exp(-value*t)
analytic=-t*f(c);numeric=(f(c+h)-f(c-h))/(2*h)
assert np.isclose(analytic,numeric,rtol=1e-8)
print('Sensitivity:',analytic,'finite difference:',numeric)''',
'The observed material regression and manufactured damping identification remain distinct experiments. A graph’s zero total exchange test does not establish physical correctness of every local flux.',
'An exactly conserved global sum can conceal wrong spatial transport. Check the local solution and boundary conditions too.',
'What does disagreement between automatic differentiation and a well-conditioned finite-difference check suggest?',
'A possible implementation, convention, differentiation-path or numerical-step issue that needs investigation. It does not by itself identify which method is wrong.')
add(30,'When is a scientific learning project ready to defend?',
'Evidence ledger: links claims to sources, assumptions and tests. Marginal guarantee: averaged over an appropriate sampling process. Independent validation: evidence not used to choose the result.',
'''A final report should identify each important statement as source-derived, analytically established, executed in a declared experiment, or still proposed. The source posts motivate useful ideas, but their strongest statements need explicit assumptions and tests. A benchmark improvement, theorem, plotted trajectory and measured sensor result are not interchangeable evidence.

Consider calibration with only nine error scores. A 99% nominal level needs rank ceil(10×.99)=10, beyond the nine available scores. The conservative interval becomes infinite. Reporting that limit is scientifically stronger than hiding it behind a finite interpolated quantile. Apply the same discipline to missing camera scale, unavailable participant IDs, unrun external comparisons and absent actual-book text.''',
'''import numpy as np
from shape_lab.evidence_v7 import conformal_rank,conformal_radius
assert conformal_rank(9,.01)==10
assert np.isinf(conformal_radius(np.arange(1,10),.01))
print('The requested extreme coverage is uninformative at this calibration size under the stated rule.')''',
'Choose an independent question using a source with suitable units, identities and a justified reuse license. The ten included industry cases are worked teaching datasets, not infinite fresh holdouts.',
'A course completion record is not certification for medicine, structural engineering, production robotics or every open research topic.',
'Which unfinished obligations must remain visible after completing this package’s reference experiments?',
'Actual-book reconciliation, deeper theorem proofs where assigned, independent projects, missing external-library comparisons, unrun model inference or paper replications, and domain-specific physical or clinical validation as relevant.')

assert [x['stage'] for x in E]==list(range(31))
for x in E:
 n=x['stage'];title=STAGES[n]['title'];folder=R/'beginner_v7'/f'{n:02d}';folder.mkdir(parents=True,exist_ok=True)
 code='''"""Exact entry check; not a substitute for a proof or a real-data experiment."""\nfrom pathlib import Path\nimport sys\nROOT=Path(__file__).resolve().parents[2]\nif str(ROOT/'src') not in sys.path:sys.path.insert(0,str(ROOT/'src'))\n'''+x['code']+'\n'
 (folder/'check.py').write_text(code)
 guide=f'''# Stage {n:02d} — {title}

## Begin with one question

**{x['question']}**

This is an entry lesson, not another course to finish first. Predict the smallest example, run its check, then continue into the original stage's deeper lesson and worked data lab. New learners can use the foundation primers whenever notation interrupts understanding.

## The words you need now

{x['vocabulary']}

## Work the example before running it

{x['explanation']}

## Test the exact calculation

From the project folder:

```bash
python beginner_v7/{n:02d}/check.py
```

The script is short enough to inspect in full:

```python
{x['code']}
```

An assertion is a condition expected to be true. If it fails, inspect the first failing claim rather than deleting the check. These are exact mathematical controls or explicit data-contract checks; passing them does not automatically establish mastery or correctness for all possible inputs. The full laboratory introduces larger examples and real observations.

## Connect it to observations

{x['bridge']}

The same idea can transfer across industries without making every dataset suitable for every model. Ask which variables, units, independent identities, timestamps or fields the proposed analysis needs. The [data catalogue](../../docs/v7/DATA_CATALOG.md) separates supplied observations, constructed controls and optional future acquisitions.

## A mistake worth catching early

{x['trap']}

## Your independent answer

{x['assignment']}

<details><summary>Reveal answer criteria after your attempt</summary>

{x['answer']}

</details>

For delayed recall, change a relevant assumption and explain whether the conclusion still holds. Merely replacing a number and copying the same reasoning is practice, not a new generalization test.

## Continue the full stage in this order

Open the [original Stage {n:02d} learning section](../../stages/{n:02d}/README.md). It links the complete lesson, slower workbook, executed lab, separate learner code, reference answers and mastery conditions. Keep those assignments; this entry guide does not replace them. Then use the [stage-specific industry transfer guide](../../industry/stage_guides/{n:02d}.md).

Save one answer in `my_work`: your original prediction, hand calculation, code/output path, explanation, a counterexample and an unsupported conclusion. Existing logs remain at `progress/learning_log_v5.json`; no entry check marks your stage assessed. See the [continuation guide](../../docs/v7/START.md) for preserving prior work.
'''
 (folder/'lesson.md').write_text(guide)
 x['title']=title;x['guide']=f'beginner_v7/{n:02d}/lesson.md';x['check']=f'beginner_v7/{n:02d}/check.py'
(R/'docs/v7/beginner_map.json').write_text(json.dumps(E,indent=2))
print('Wrote 31 distinct beginner entry lessons and 31 standalone runnable checks.')
