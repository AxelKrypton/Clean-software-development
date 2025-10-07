import numpy

input_0 = ([1.0, 0.0, 0.0],
           [0.0, 1.0, 0.0],
           [0.0, 0.0, 1.0])
expected_0 = ([2.0 * numpy.pi, 0.0, 0.0],
              [0.0, 2.0 * numpy.pi, 0.0],
              [0.0, 0.0, 2.0 * numpy.pi],
              numpy.column_stack([[2.0 * numpy.pi, 0.0, 0.0],
                                  [0.0, 2.0 * numpy.pi, 0.0],
                                  [0.0, 0.0, 2.0 * numpy.pi]]))

input_1 = ([1.0, 0.0, 0.0],
           [1.0, 0.0, 0.0],
           [1.0, 0.0, 0.0])
expected_1 = None

testdata = [(input_0, expected_0, False), (input_1, expected_1, True)]
