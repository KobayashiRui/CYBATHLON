from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

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

print("start")
angle = my_chain.inverse_kinematics([
    [1, 0, 0, 0],
    [0, 1, 0, 0.3],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
    ])
print(angle)

angle = my_chain.inverse_kinematics([
    [1, 0, 0, 0],
    [0, 1, 0, 0.5],
    [0, 0, 1, 1],
    [0, 0, 0, 1]
    ])
print(angle)
