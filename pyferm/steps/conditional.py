from . import brewstep


class conditional(brewstep):
    pass


#   - name: 50% attenuation
#     class: pyferm.steps.conditional.conditional
#     conditions:
#       - input: my_tilt.metric[1]
#         value: 1.050
#         threshold: 1, 1
#     triggers:
#       - input: my_tilt.metric[0]
#         value: 70
#         threshold: 1, 1

# if triggers are met, then start
# do the thing, for interval do duration, for conditional check conditions
# if conditions are met, move to next step
