from makeboard import createboard

def test_createboard():
    dimensions = 10
    max_mines = 10
    assert createboard(dimensions,max_mines) != [[' ' for i in range(dimensions)] for j in range(dimensions)]