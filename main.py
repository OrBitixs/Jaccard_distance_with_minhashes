import argparse
import random

def create_char_matrix(num_doc: int, num_elemen: int, num_hash: int) -> list[list[int]]:
    matrix = []
    for el in range(num_elemen):
        matrix.append([random.randint(0,1) for i in range(num_doc)])

    hash_coef = get_prime_numbers(11, num_hash)
    for el in range(num_elemen):
        for h in range(num_hash):
            new_hash = (((el+h))*hash_coef[h])%num_elemen
            # print(new_hash, end="\t")
            matrix[el].append(new_hash)
        # print()

    return matrix

def pretty_matrix_print(label:str, row_labels: list[str], column_labels: list[str], matrix: list[list]) -> int:
    print("\n{}".format(label))

    if matrix.__len__() != row_labels.__len__() or matrix[0].__len__() != column_labels.__len__():
        print("{}: got wrong row or column labels".format(label))
        return -1

    # print column labels
    print("\t|", end="")
    for label in column_labels:
        print(label+"\t|", end="")
    print()

    # print row labels and cells
    for row_id in range(row_labels.__len__()):
        print("-"*8*(column_labels.__len__()+1)+"-")
        print(row_labels[row_id] + "\t|", sep="", end="")
        for column_id in range(column_labels.__len__()):
            print(str(matrix[row_id][column_id])[0:min(6, str(matrix[row_id][column_id]).__len__())], "\t|", sep="", end="")
        print()

    return 0

def get_prime_numbers(start: int, number: int) -> list[int]:
    prime_list = []
    current = start
    while prime_list.__len__() < number:
        for i in range(2, current//2+1):
            if current % i == 0:
                break
        else:
            prime_list.append(current)
        current+=1

    return prime_list

def create_sig_matrix(num_doc: int, num_hash: int, max: int) -> list[list[int]]:
    matrix = []
    for _ in range(num_hash):
        matrix.append([max for _ in range(num_doc)])
    return matrix

def update_sig_matrix(sig_matrix: list[list[int]], char_matrix: list[list[int]]) -> list[list[int]]:
    for it_char_row_id in range(char_matrix.__len__()):
        for char_column_id in range(sig_matrix[0].__len__()):
            if char_matrix[it_char_row_id][char_column_id] == 1:
                for sig_row_id in range(sig_matrix.__len__()):
                    sig_matrix[sig_row_id][char_column_id] = min(sig_matrix[sig_row_id][char_column_id], char_matrix[it_char_row_id][args.documents+sig_row_id])

    return sig_matrix

def jaccard_sig(sig_matrix: list[list[int]]) -> list[list[int]]:
    similarity_matrix = []
    for i in range(sig_matrix[0].__len__()):
        similarity_matrix.append([])
        for _ in range(i+1):
            similarity_matrix[i].append(-1)
        for j in range(i+1, sig_matrix[0].__len__()):

            unique = set()
            # print(unique)
            equal = 0
            for row in range(sig_matrix.__len__()):
                unique.add(sig_matrix[row][i])
                unique.add(sig_matrix[row][j])
                if sig_matrix[row][i] == sig_matrix[row][j]:
                    equal += 1

            similarity_matrix[i].append(equal/sig_matrix.__len__())

    similarity_matrix.pop()

    return similarity_matrix

def jaccard_char(char_matrix: list[list[int]], column_num: int):
    similarity_matrix = []
    for i in range(column_num):
        similarity_matrix.append([])
        for _ in range(i+1):
            similarity_matrix[i].append(-1)
        for j in range(i+1, column_num):
            equal = 0
            filled = 0
            for row in range(char_matrix.__len__()):
                if char_matrix[row][i] == 1 or char_matrix[row][j] == 1:
                    filled += 1
                    if char_matrix[row][i] == char_matrix[row][j]:
                        equal += 1

            similarity_matrix[i].append(equal/filled)

    similarity_matrix.pop()

    return similarity_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate distance between documents")

    parser.add_argument("-d", "--document", dest="documents", metavar="DOCUMENTS_NUM",
                        type=int, help="Number of documents to be compared", default=4)
    parser.add_argument("-e", "--element", dest="elements", metavar="ELEMENTS_NUM",
                        type=int, help="Number of elements in alphabet", default=5)
    parser.add_argument("--hash",  dest="hash_functions", metavar="HASH_FUNCTION_NUM",
                        type=int, help="Number of hash functions used to calculate distance", default=6)

    args = parser.parse_args()
    # print(args.documents, args.elements, args.hash_functions)

    char_matrix = create_char_matrix(args.documents, args.elements, args.hash_functions)

    c_labels = ["S" + str(dc) for dc in range(args.documents)]
    c_labels.extend(["h"+str(h) for h in range(args.hash_functions)])
    pretty_matrix_print("Characteristic matrix", [str(el) for el in range(args.elements)], c_labels, char_matrix)
    # print(get_prime_numbers(10, 10))

    sig_matrix = create_sig_matrix(args.documents, args.hash_functions, args.elements)
    sig_matrix = update_sig_matrix(sig_matrix, char_matrix)

    pretty_matrix_print("Signature matrix", ["h"+str(h) for h in range(sig_matrix.__len__())], ["S"+str(dc) for dc in range(sig_matrix[0].__len__())], sig_matrix)

    jaccard_sig_matrix = jaccard_sig(sig_matrix)
    # print(jaccard_sig_matrix)
    pretty_matrix_print("Jaccard from signature matrix", ["S"+str(h) for h in range(jaccard_sig_matrix.__len__())], ["S"+str(dc) for dc in range(jaccard_sig_matrix[0].__len__())], jaccard_sig_matrix)

    jaccard_char_matrix = jaccard_char(char_matrix, args.documents)
    pretty_matrix_print("Jaccard from characteristic matrix", ["S"+str(h) for h in range(jaccard_char_matrix.__len__())], ["S"+str(dc) for dc in range(jaccard_char_matrix[0].__len__())], jaccard_char_matrix)
