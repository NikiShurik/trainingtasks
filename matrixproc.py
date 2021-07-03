class Matrix():
    n = 0  # num of rows
    m = 0  # num of columns
    struct = []  # matrix
    type_inside = "int"

    # _________________ initialize matrix ___________________________
    # create structure n * m initiated by zeros
    def build_struct(self):
        return [[0 for i in range(self.m)] for j in range(self.n)]

    # kwarg:
    # 'n' - number of rows
    # 'm' number of columns
    # 'data' - string of elements separated by space
    def __init__(self, **kwarg):
        if ('n' in kwarg) and ('m' in kwarg) and ('data' in kwarg):
            self.n = int(kwarg['n'])
            self.m = int(kwarg['m'])
            self.struct = self.build_struct()
            if ('.' in kwarg['data']) or (',' in kwarg['data']):
                self.type_inside = "float"
            else:
                self.type_inside = "int"
            datalist = kwarg['data'].split(' ')
            for i in range(self.n):
                for j in range(self.m):
                    #print(f'len datalist {len(datalist)}')
                    #print(f'self.struct[{i}][{j}] = datalist[{j} + {i} * {(self.m)}]')
                    if self.type_inside == "float":
                        self.struct[i][j] = float(datalist[j + i * (self.m)])
                    else:
                        self.struct[i][j] = int(datalist[j + i * (self.m)])
        elif ('struct' in kwarg) and ('i' in kwarg) and ('j' in kwarg):
            i = kwarg['i']
            j = kwarg['j']
            struct = kwarg['struct']
            self.n = len(struct) - 1
            self.m = len(struct[i]) - 1
            self.struct = self.build_struct()
            for x in range(len(struct)):
                if x < i:
                    for y in range(len(struct[i])):
                        if y < j:
                            self.struct[x][y] = kwarg['struct'][x][y]
                        elif y > j:
                            self.struct[x][y-1] = kwarg['struct'][x][y]
                elif x > i:
                    for y in range(len(struct[i])):
                        if y < j:
                            self.struct[x-1][y] = kwarg['struct'][x][y]
                        elif y > j:
                            self.struct[x-1][y-1] = kwarg['struct'][x][y]
            #self.print()
        elif ('struct' in kwarg) and ('i' not in kwarg) and ('j' not in kwarg):
            self.struct = kwarg['struct']
            self.n = len(self.struct)
            self.m = len(self.struct[0])
        else:
            print('The operation cannot be performed.\n')
    # print(mat1.struct) print matrix as shown:
    # 1 2 3
    # 4 5 6
    # 7 8 9
    def print(self):
        for i in range(self.n):
            row = ''
            for j in range(self.m):
                el = self.struct[i][j]
                row += str(el)
                if j < (self.m - 1):
                    row = row + ' '
            print(row)
        print('')

    # override methods for operations
    def __add__(self, other):
        """Addition of matrix."""
        line = ''
        if (self.n == other.n) and (self.m == other.m):
            for i in range(self.n):
                if line != '':
                    line = line + ' '
                for j in range(self.m):
                    line = line + str(self.struct[i][j] + other.struct[i][j])
                    if j < (self.m - 1):
                        line = line + ' '
            matarg = {'n': self.n,  # - number of rows
                      'm': self.m,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            return Matrix(**matarg)
        else:
            print("The operation cannot be performed.\n")
            return None  # fill it

    def __mul__(self, other):
        if (self.m == other.n):
            line = ''
            #print(f"matrix 1:{self.struct}\n")
            #print(f"matrix 2:{other.struct}\n")
            for i in range(self.n):
                if line != '':
                    line = line + ' '
                for j in range(other.m):
                    el = 0
                    for k in range(self.m):
                        #print(f'self.struct[{i}][{k}] * other.struct[{k}][{j}]')
                        el += self.struct[i][k] * other.struct[k][j]
                    line = line + str(el)
                    if j < (other.m - 1):
                        line = line + ' '
            matarg = {'n': self.n,  # - number of rows
                      'm': other.m,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            #print(f"matarg -> {matarg}")
            return Matrix(**matarg)
        else:
            print("The operation cannot be performed.\n")
            return None  # fill it

    # умножение слева приравнивается к умножению на скаляр
    def __rmul__(self, other):
        line = ''
        for i in range(self.n):
            if line != '':
                line = line + ' '
            for j in range(self.m):
                line = line + str(self.struct[i][j] * other)
                if j < (self.m - 1):
                    line = line + ' '
        matarg = {'n': self.n,  # - number of rows
                  'm': self.m,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        return Matrix(**matarg)

    def transpose(self):
        line = ''
        for i in range(self.n):
            if line != '':
                line = line + ' '
            for j in range(self.m):
                line = line + str(self.struct[j][i])
                if j < (self.m - 1):
                    line = line + ' '
        matarg = {'n': self.m,  # - number of rows
                  'm': self.n,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        return Matrix(**matarg)

    def transposevert(self):
        line = ''
        for i in range(self.n):
            if line != '':
                line = line + ' '
            for j in range((self.m), 0, -1):
                #print(f'struct[{j}][{i}]')
                line = line + str(self.struct[i][j-1])
                if j > 1:  #< (self.m - 1):
                    line = line + ' '
        matarg = {'n': self.n,  # - number of rows
                  'm': self.m,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        #print(matarg)
        return Matrix(**matarg)

    def transposehor(self):
        line = ''
        for i in range((self.n), 0, -1):
            if line != '':
                line = line + ' '
            for j in range(self.m):
                #print(f'struct[{j}][{i}]')
                line = line + str(self.struct[i-1][j])
                if j < (self.m - 1): #j > 1:
                    line = line + ' '
        matarg = {'n': self.n,  # - number of rows
                  'm': self.m,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        #print(matarg)
        return Matrix(**matarg)

    def transposeside(self):
        line = ''
        for i in range(self.n, 0, -1):
            if line != '':
                line = line + ' '
            for j in range(self.m, 0, -1):
                line = line + str(self.struct[j-1][i-1])
                if j > 1:
                    line = line + ' '
        matarg = {'n': self.m,  # - number of rows
                  'm': self.n,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        return Matrix(**matarg)

    def det(self):
        # проверить условие применимости определения детерминанта
        # если не применимо то возврат None
        # проверить условие выхода если полученная матрица = 1*1
        # проверить условие выхода если полученная матрица = 2*2
        if self.n != self.m:
            print('The operation cannot be performed.\n')
            return None
        elif self.n == 2:
            return self.struct[0][0] * self.struct[1][1] - self.struct[1][0] * self.struct[0][1]
        elif self.n == 1:
            return self.struct[0][0]
        else:
            tmp = 0
            for k in range(self.n):
                tmp += pow(-1, (k+2)) * self.struct[0][k] * Matrix(**{'struct': self.struct, 'i': 0, 'j': k}).det()
            return tmp

    def inv(self):
        struct = self.build_struct()
        for i in range(self.n):
            for j in range(self.m):
                struct[i][j] = pow((-1),(i+j+2)) * Matrix(**{'struct': self.struct, 'i': i, 'j': j}).det()
        mat = Matrix(**{'struct': struct})
        return (1/self.det()) * mat.transpose()


# function prepare data for matrix constructor -
# make from input receive a n strings as a list of strings and
# transform it in 1 string of elements separated by ' ' (space)
def enter_data_for_mat(n, m):
    line = ''
    for i in range(n):
        if line != '':
            line = line + ' '
        # f'INPUT LINE {i}:' - input info add in input() to debug
        dat = input()
        line = line + dat
    return line

class Interface():
    messages = {
        'main': "1. Add matrices\n2. Multiply matrix by a constant\n3. Multiply matrices\n4. Transpose matrix\n"
                "5. Calculate a determinant\n6. Inverse matrix\n0. Exit",
        'offline': "",
    }
    state = 'main'

    def functionadd(self):
        line = input("Enter size of first matrix: ")
        list1 = line.split()
        n1 = int(list1[0])
        m1 = int(list1[1])
        print("Enter first matrix:")
        line = enter_data_for_mat(n1, m1)
        matarg = {'n': n1,  # - number of rows
                  'm': m1,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat1 = Matrix(**matarg)
        line = input("Enter size of second matrix: ")
        list1 = line.split()
        n2 = int(list1[0])
        m2 = int(list1[1])
        print("Enter second matrix:")
        line = enter_data_for_mat(n2, m2)
        matarg = {'n': n2,  # - number of rows
                  'm': m2,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat2 = Matrix(**matarg)
        mat3 = mat1 + mat2
        if mat3 != None:
            print("The result is:")
            mat3.print()
        return

    def functionconstmul(self):
        line = input("Enter size of matrix: ")
        list1 = line.split()
        n1 = int(list1[0])
        m1 = int(list1[1])
        print("Enter matrix:")
        line = enter_data_for_mat(n1, m1)
        matarg = {'n': n1,  # - number of rows
                  'm': m1,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat1 = Matrix(**matarg)
        const = float(input("Enter constant: "))
        mat2 = const * mat1
        print("The result is:")
        mat2.print()
        return

    def functionmul(self):
        line = input("Enter size of first matrix: ")
        list1 = line.split()
        n1 = int(list1[0])
        m1 = int(list1[1])
        print("Enter first matrix:")
        line = enter_data_for_mat(n1, m1)
        matarg = {'n': n1,  # - number of rows
                  'm': m1,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat1 = Matrix(**matarg)
        line = input("Enter size of second matrix: ")
        list1 = line.split()
        n2 = int(list1[0])
        m2 = int(list1[1])
        print("Enter second matrix:")
        line = enter_data_for_mat(n2, m2)
        matarg = {'n': n2,  # - number of rows
                  'm': m2,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat2 = Matrix(**matarg)
        mat3 = mat1 * mat2
        if mat3 != None:
            print("The result is:")
            mat3.print()
        return

    def functiontranspose(self):
        print('1. Main diagonal\n2. Side diagonal\n3. Vertical line\n4. Horizontal line')
        querry = input("Your choice: ")
        if querry == '1':
            line = input("Enter matrix size: ")
            list1 = line.split()
            n1 = int(list1[0])
            m1 = int(list1[1])
            print("Enter matrix:")
            line = enter_data_for_mat(n1, m1)
            matarg = {'n': n1,  # - number of rows
                      'm': m1,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            mat1 = Matrix(**matarg)
            mat2 = mat1.transpose()
            if mat2 != None:
                print("The result is:")
                mat2.print()
            self.state = 'main'
        if querry == '2':
            line = input("Enter matrix size: ")
            list1 = line.split()
            n1 = int(list1[0])
            m1 = int(list1[1])
            print("Enter matrix:")
            line = enter_data_for_mat(n1, m1)
            matarg = {'n': n1,  # - number of rows
                      'm': m1,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            mat1 = Matrix(**matarg)
            mat2 = mat1.transposeside()
            if mat2 != None:
                print("The result is:")
                mat2.print()
            self.state = 'main'
        if querry == '3':
            line = input("Enter matrix size: ")
            list1 = line.split()
            n1 = int(list1[0])
            m1 = int(list1[1])
            print("Enter matrix:")
            line = enter_data_for_mat(n1, m1)
            matarg = {'n': n1,  # - number of rows
                      'm': m1,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            mat1 = Matrix(**matarg)
            mat2 = mat1.transposevert()
            if mat2 != None:
                print("The result is:")
                mat2.print()
            self.state = 'main'
        if querry == '4':
            line = input("Enter matrix size: ")
            list1 = line.split()
            n1 = int(list1[0])
            m1 = int(list1[1])
            print("Enter matrix:")
            line = enter_data_for_mat(n1, m1)
            matarg = {'n': n1,  # - number of rows
                      'm': m1,  # - number of columns
                      'data': line,  # string of elements separated by space
                      }
            mat1 = Matrix(**matarg)
            mat2 = mat1.transposehor()
            if mat2 != None:
                print("The result is:")
                mat2.print()
            self.state = 'main'
        return

    def det(self):
        line = input("Enter matrix size: ")
        list1 = line.split()
        n1 = int(list1[0])
        m1 = int(list1[1])
        print("Enter matrix:")
        line = enter_data_for_mat(n1, m1)
        matarg = {'n': n1,  # - number of rows
                  'm': m1,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat1 = Matrix(**matarg)
        print("The result is:")
        print(mat1.det())
        return

    def inverse(self):
        line = input("Enter matrix size: ")
        list1 = line.split()
        n1 = int(list1[0])
        m1 = int(list1[1])
        print("Enter matrix:")
        line = enter_data_for_mat(n1, m1)
        matarg = {'n': n1,  # - number of rows
                  'm': m1,  # - number of columns
                  'data': line,  # string of elements separated by space
                  }
        mat1 = Matrix(**matarg)
        if mat1.det() != 0:
            invmat = mat1.inv()
            invmat.print()
        else:
            print("This matrix doesn't have an inverse.")

    def process(self, querry):
        if self.state == 'main':
            if querry == '0':
                self.state = 'offline'
            elif querry == '1':
                self.functionadd()
                self.state = 'main'
            elif querry == '2':
                self.functionconstmul()
                self.state = 'main'
            elif querry == '3':
                self.functionmul()
                self.state = 'main'
            elif querry == '4':
                self.functiontranspose()
                self.state = 'main'
            elif querry == '5':
                self.det()
                self.state = 'main'
            elif querry == '6':
                self.inverse()
                self.state = 'main'
            else:
                self.state = 'main'
        return

term = Interface()
print(term.messages[term.state])
while term.state != 'offline':
    querry = input("Your choice: ")
    term.process(querry)
    if term.state != 'offline':
        print(term.messages[term.state])
