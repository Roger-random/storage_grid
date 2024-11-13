# Storage Grid

Parametrically generate small storage trays that fit together.

![storage grid under evaluation with half drawer of fasteners](./img/storage%20grid%20under%20evaluation%20with%20half%20drawer%20of%20fasteners.jpg)

_Drawer of fasteners showing partial adoption, before (right) and after (left)_

### Parametric Solids

Size of each cell on the grid can be adjusted from default of 15mm by 15mm,
and from there trays are specified in number of grid cells they occupy.
This example is a 4x4 tray.

![Example 4x4 storage tray](./img/storage%20grid%20tray%204x4.png)

By default, generated STLs are solid shapes intended for 3D printing in a
special mode that may be named "single-wall", "spiral", or "vase mode"
depending on slicer software used. If that is not strong enough, an optional
thickness parameter may be specified to generate STL with thicker walls to
be printed normally.

### Dovetailed sides

Trays have dovetails to fit into each other. These were designed for sitting
in a drawer. The dovetails ensure the trays hold their relative positions
and not slide around as the drawer is opened and closed.

Deliberate gaps can be added to allow individual trays to be easily removed.
The dovetails ensure their space will remain open awaiting their return.

Alternatively trays can be generated without any gaps, so they fit tightly
together to assemble a single large organizer.

# Usage

This project was written with CadQuery
(https://cadquery.readthedocs.io/en/stable/index.html)
and there are multiple options for running this code, see below.

In all cases you will need to have basic understanding of Python programming
language in order to customize parameters to suit your project.

## Step 1: Decide Grid Cell Size

Every storage tray STL output by the generator is sized to fit a common grid,
so the first decision is the size of each cell in that grid. The default size
of 15mm x 15mm should work for most scenarios, but can be fine-tuned.

Example: if the goal is to tightly fill a 160mm x 180mm box, it may make sense
to use a cell size of 16mm x 18mm so the box is evenly divided into a 10 x 10
grid.

Normal Range: Grid cell size a few millimeters larger or smaller than default
of 15mm (~12mm-~18mm) should work well. Significant changes beyond that may
will require adjusting dovetail dimensions to suit. Larger grid cell sizes
may result in long flat sides, which risks warping during vase mode printing.
To avoid this, consider using smaller cell sizes to generate same size trays.

## Step 2: Decide Tray Height

Each tray should be at least double the cell size. So at default cell size of
15mm x 15mm, trays should be 30mm tall or taller for all the relevant geometry
calculations to work. That calculation does not place an upper bound so maximum
height would be dictated by practicalities like user-friendliness, 3D printer
capability, the storage voluem, etc.

There's nothing special about the default value of 75mm. That just happens to
be the height of the storage drawer I wanted to organize.

## Step 3: Decide Gap Size (Tightness of Fit)

By default the trays are generated with a small gap all around so they can be
individually removed, used, and placed back in their slot. Alternatively, the
gap can be set to zero so all generated trays fit tightly together and
assemble into a larger organizer tray.

## Step 4: Create Generator Instance

Once those basic decisions have been made, create an instance of the generator
class with chosen values.

```
from dovetailstoragegrid import DovetailStorageGrid as dsg

# These are the default values, presented as example. Units in mm
dsg_01 = dsg(x = 15, y = 15, z = 75, tray_gap = 0.1)

```

Additional fine-tuning parameters are available, but you can leave them at
their defaults for initial experimentation. See code comments for details.

## Step 5: Generate Trays

Once the generator class has been created, call one of its methods to generate
a CadQuery shape based on parameters.

### Label Tray

```
tray = dsg_01.label_tray(2, 3)
```

Tray with a small angled surface at its top front, designed for a label and
can also serve as a small handle for lifting that tray via fingertip.

The first two parameters are required, specifying the number of grid cells
this tray would occupy. In this example, Parameters `(2,3)` generates a 2x3
tray. Given the cell size of 15mm x 15mm, this results in a 30mm x 45mm tray.

Optional parameter `wall_thickness` defaults to zero, which generates a solid
shape that is intended to be printed in vase mode. Alternative it can be
exported to another CAD software for further customization, where you can
cut whatever features you want to generate a custom tray that has dovetails to
fit with other trays on the storage grid.

If vase mode printing is not strong
enough, specify a nonzero wall thickness in mm. Recommend a multiple of your
3D printer nozzle size. So for the typical 0.4mm nozzle, `wall_thickness=0.8`
will result in two perimeter layer wall. `wall_thickness=1.2` for three
perimeter wall, etc.

### Basic Tray

```
tray = dsg_01.basic_tray(2, 3)
```
A basic tray doesn't have a small label area in front, which may be desirable
especially for the export-and-modify usage scenario. All other parameters are
identical to those for label tray.

# Running the Generator

### Option 1: CadQuery graphical interface CQ-Editor

For interactive creation and easy visualization, installing CQ-Editor on your
computer allows CadQuery experimentation with immediate rendered feedback.
Follow CadQuery installation instructions for CQ-Editor, which will install
all necessary CadQuery dependencies.
https://cadquery.readthedocs.io/en/stable/installation.html#adding-a-nicer-gui-via-cq-editor

Then launch CQ-Editor and open `for_cq-editor.py` in this repository. From
the "Run" menu select "Render" to see the example in action. Adjust parameters
and select "Render" again to see their effects. Once you are happy with the
results, click on the rendered tray and select "Tools"/"Export as STL" to
generate a STL file for 3D printing.

### Option 2: Run CadQuery at command line

If you want to generate a large set of trays and don't want to individually
click and export from CQ-Editor, you can set up a Python environment
with CadQuery using either conda or pip.
https://cadquery.readthedocs.io/en/stable/installation.html

Once up and running, modify `for_command_line.py` in this repository as needed
to suit your scenario and generate the specified set of STL files.

`python for_command_line.py`

### Option 3: Cloud Hosted Jupyter

If you don't want to install software onto your own computer, you can use
somebody else's computer a.k.a. a cloud service.

Because this is all Python, we can take advantage of Python's current
popularity partially thanks to AI mania. Jupyter (https://jupyter.org/)
makes Python easily accessible via a web browser and there are several Jupyter-
based cloud services. Hosted by various companies to entice newcomers
to explore machine learning under that company's umbrella. Which is great,
but for our purposes we'll just use their Python runtime and ignore their
magical AI special sauce.

The following instructions are for one particular service,
[Google Colab](https://colab.research.google.com/) but should be similar
for other Jupyter services. The tricky part is installing CadQuery into the
hosted environment, as different providers will have different restrictions
on what external libraries are permitted.

As of this writing, Google Colab has a free tier sufficient to run this project.
As does [GitHub Codespaces](https://github.com/codespaces).
The free tier seems to have disappeared from
[AWS SageMaker](https://aws.amazon.com/pm/sagemaker/),
but there is a free trial period.
And of course there are other cloud-hosted Jupyter services.

Anyway, instructions for Google Colab:
1. Log into your Google account.
2. Open a new browser window to https://colab.research.google.com/
3. Click "New notebook".
4. Go to the "File" menu and select "Open notebook"
5. Click "GitHub"
6. Enter URL for this project's Jupyter example: https://github.com/Roger-random/storage_grid/blob/main/for_jupyter.ipynb
7. Go to the left toolbar and click on the file folder icon. If you are not
automatically connected to a free tier runtime at this point, you will need to
do so manually before the file explorer becomes available.
8. Click the single file icon for "Upload to session storage"
9. Upload a copy of `dovetailstoragegrid.py` from this repository.
10. Follow instructions in the example notebook step by step, or select
"Runtime"/"Run all" to run the entire example in a single shot.
