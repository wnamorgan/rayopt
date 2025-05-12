# Optical Ray Tracing Software Architecture

## Class Hierarchy
System  
├── manages → list[Element]  
└── propagates Ray through Elements

Element (abstract)  
├── has → Geometry (optional composition)  
├── has → SurfaceBehavior (optional composition)  
├── defines abstract: intersect(), redirect()  
└── subclasses: MirrorElement, LensElement, DetectorElement, etc.  

Geometry (optional, abstract if used)  
├── defines abstract: F(), gradient(), intersect()  
└── subclasses: PlaneGeometry, SphereGeometry, AsphereGeometry, CylinderGeometry, etc.  

SurfaceBehavior (optional, abstract if used)  
├── defines abstract: redirect()  
└── subclasses: Reflective, Refractive, Absorbing, Lambertian, etc.  

Ray  
├── origin: np.ndarray  
├── direction: np.ndarray  
├── methods: point(t), offset(epsilon)  

Hit (optional, used in intersect)  
├── t: float  
├── point: np.ndarray  
├── normal: np.ndarray  
├── element: Element  

---

## `System` Class

**Attributes:**
- `elements: list[Element]`
- `max_bounces: int`
- `epsilon: float`

**Methods:**
- `propagate(ray: Ray) -> list[Ray]`  
  Repeatedly find nearest element, redirect ray, and collect propagation history.
- `find_next_intersection(ray: Ray) -> Hit or None`  
  Evaluate all elements and return the closest valid intersection.

---

## `Element` Class (abstract)

**Abstract Methods:**
- `intersect(ray: Ray) -> float or None`  
  Return distance `t` to intersection point, or `None` if no intersection.
- `redirect(ray: Ray, t: float) -> tuple[Ray, bool]`  
  Return a redirected ray and a boolean flag indicating continuation.

**Concrete Subclasses May Include:**
- `MirrorElement`
- `RefractiveElement`
- `LambertianElement`
- `DetectorElement`

---

## `Geometry` Class (optional, abstract)

**Abstract Methods:**
- `F(point: np.ndarray) -> float`  
  Implicit surface constraint function.
- `gradient(point: np.ndarray) -> np.ndarray`  
  Surface normal.
- `intersect(ray: Ray) -> float or None`  
  Return intersection `t` with the ray.

**Possible Subclasses:**
- `PlaneGeometry`
- `SphereGeometry`
- `AsphereGeometry`
- `CylinderGeometry`

---

## `SurfaceBehavior` Class (optional)

**Abstract Method:**
- `redirect(ray: Ray, point: np.ndarray, normal: np.ndarray) -> tuple[Ray, bool]`

**Subclasses:**
- `Reflective`
- `Refractive`
- `Lambertian`
- `Absorbing`
- `Detector`

---

## `Ray` Class

**Attributes:**
- `origin: np.ndarray`
- `direction: np.ndarray`

**Methods:**
- `point(t: float) -> np.ndarray`  
  Return a point on the ray.
- `offset(epsilon: float) -> Ray`  
  Return a slightly offset ray (to avoid self-intersection).

---

## `Hit` Class (optional)

**Attributes:**
- `t: float`
- `point: np.ndarray`
- `normal: np.ndarray`
- `element: Element`

Used to store and return intersection information from `intersect()`.

---

## Optional Extensions

- `RayBundle`: Manage collections of rays in simulation.
- `SceneVisualizer`: Plot rays and surfaces using `matplotlib`.
- `EnergyTracker`: Track flux or reflectance through elements.
- `Material`: Optional physical properties like index vs. wavelength.

