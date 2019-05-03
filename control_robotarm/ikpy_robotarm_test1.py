from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D 
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

my_chain = Chain(name='cybathlon', links=[
    URDFLink(
      name="joint1",
      translation_vector=[0,0,0],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="joint2",
      translation_vector=[0,0,0.075],
      orientation=[0, 0, 0],
      rotation=[1, 0, 0],
    ),
    URDFLink(
      name="joint3",
      translation_vector=[0.045, 0, 0.802],
      orientation=[0, 0, 0],
      rotation=[0, 1, 0],
    ),
    URDFLink(
      name="joint4",
      translation_vector=[-0.045, 0, 0.746],
      orientation=[0, 0, 0],
      rotation=[0, 0, 0],
    )
])

my_chain.plot(my_chain.inverse_kinematics([
    [1, 0, 0, -0.3],
    [0, 1, 0, 0.3],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
    ]), ax)
#my_chain.plot([0,0,0],ax)
matplotlib.pyplot.show()
