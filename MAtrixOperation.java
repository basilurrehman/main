import java.util.Scanner;

public class MatrixOperations {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[][] Mat_1 = new int[3][3];
        int[][] Mat_2 = new int[3][3];
        System.out.println("Enter values for Matrix Mat_1 (3x3): ");
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                Mat_1[i][j] = scanner.nextInt();
            }
        }
        System.out.println("Enter values for Matrix Mat_2 (3x3): ");
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                Mat_2[i][j] = scanner.nextInt();
            }
        }
        int[][] result = new int[3][3];
        int[][] Mat_1_cubed = matsrixPower(Mat_1, 3);
        int[][] Mat_2_squared = matrixPower(Mat_2, 2);
        int[][] Mat_2_minus_3_squared = matrixSubtractAndSquare(Mat_2, 3);
        int[][] Mat_2_fifth = matrixPower(Mat_2, 5);
        int[][] Mat_1_minus_2 = matrixSubtract(Mat_1, 2);
        result = matrixAdd(matrixAdd(matrixAdd(Mat_1_cubed, Mat_2_squared), Mat_2_minus_3_squared), matrixSubtractMatrices(Mat_2_fifth, Mat_1_minus_2));
        System.out.println("Resulting Matrix: ");
        printMatrix(result);
        scanner.close();
    }
    public static int[][] matrixPower(int[][] mat, int power) {
        int[][] result = mat;
        for (int i = 1; i < power; i++) {
            result = matrixMultiply(result, mat);
        }
        return result;
    }
    public static int[][] matrixSubtractAndSquare(int[][] mat, int value) {
        int[][] result = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = (mat[i][j] - value) * (mat[i][j] - value);
            }
        }
        return result;
    }
    public static int[][] matrixSubtract(int[][] mat, int value) {
        int[][] result = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = mat[i][j] - value;
            }
        }
        return result;
    }
    public static int[][] matrixSubtractMatrices(int[][] mat1, int[][] mat2) {
        int[][] result = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = mat1[i][j] - mat2[i][j];
            }
        }
        return result;
    }
    public static int[][] matrixAdd(int[][] mat1, int[][] mat2) {
        int[][] result = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = mat1[i][j] + mat2[i][j];
            }
        }
        return result;
    }
    public static int[][] matrixMultiply(int[][] mat1, int[][] mat2) {
        int[][] result = new int[3][3];
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                result[i][j] = 0;
                for (int k = 0; k < 3; k++) {
                    result[i][j] += mat1[i][k] * mat2[k][j];
                }
            }
        }
        return result;
    }
    public static void printMatrix(int[][] mat) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(mat[i][j] + " ");
            }
            System.out.println();
        }
    }
}
