from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D 
ax = matplotlib.pyplot.figure().add_subplot(111, projection='3d')

#my_chain = Chain.from_urdf_file("test_robot.URDF")
my_chain = Chain.from_urdf_file("cybathlon_robotarm.URDF")

print("start")
print(my_chain)
#my_chain.plot(my_chain.inverse_kinematics([
#    [1, 0, 0, 5],
#    [0, 1, 0, 0],
#    [0, 0, 1, -5],
#    [0, 0, 0, 1]
#    ]),ax)
#matplotlib.pyplot.show()
#print(my_chain.inverse_kinematics([
#    [1, 0, 0, 5],
#    [0, 1, 0, 0],
#    [0, 0, 1, -5],
#    [0, 0, 0, 1]
#    ]))
my_chain.plot([0,0,0,0],ax)
matplotlib.pyplot.show()