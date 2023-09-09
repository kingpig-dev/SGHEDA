import vtk

# Create a pipe geometry
outer_radius = 0.2
inner_radius = 0.1
length = 1.0
resolution = 30

# Create the pipe source
pipe_source = vtk.vtkCylinderSource()
pipe_source.SetRadius(outer_radius)
pipe_source.SetHeight(length)
pipe_source.SetResolution(resolution)

# Create the inner cylinder
inner_cylinder = vtk.vtkCylinderSource()
inner_cylinder.SetRadius(inner_radius)
inner_cylinder.SetHeight(length)
inner_cylinder.SetResolution(resolution)

# Combine the outer and inner cylinders using a boolean operation
boolean_operation = vtk.vtkImplicitBoolean()
boolean_operation.SetOperationTypeToDifference()
boolean_operation.AddFunction(pipe_source.GetOutput())
boolean_operation.AddFunction(inner_cylinder.GetOutput())

# Create an isosurface
isosurface = vtk.vtkContourFilter()
isosurface.SetInputConnection(boolean_operation.GetOutputPort())
isosurface.SetValue(0, 0.5)  # Set the isovalue to 0.5

# Create a mapper and actor for the isosurface
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(isosurface.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Create a renderer and render window
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1.0, 1.0, 1.0)  # Set background color to white

render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)  # Set window size

# Create an interactor and set the render window
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Enable user interaction
interactor.Initialize()
interactor.Start()