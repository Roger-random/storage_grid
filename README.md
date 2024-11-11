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
and there are multiple options for usage, see below.

In all cases you will need to have basic understanding of Python programming
language in order to customize parameters to suit your project.

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
hosted environment, as different providers will have different restrictions.

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
