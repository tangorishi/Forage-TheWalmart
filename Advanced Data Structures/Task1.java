import java.util.Arrays;
import java.util.NoSuchElementException;

public class PowerHeap {
    private double power;
    private int size;
    private int[] heapArray;

    // Constructor
    public PowerHeap(double power, int capacity) {
        this.size = 0;
        heapArray = new int[capacity + 1];
        this.power = power;
        Arrays.fill(heapArray, -1);
    }

    private int getParentIndex(int childIndex) {
        return (int) ((childIndex - 1) / Math.pow(2, power));
    }

    public boolean isFull() {
        return size == heapArray.length;
    }

    public void insert(int value) {
        if (isFull()) {
            throw new NoSuchElementException("Heap is full, no space to insert new element.");
        } else {
            heapArray[size++] = value;
            heapifyUp(size - 1);
        }
    }

    private void heapifyUp(int index) {
        int temp = heapArray[index];
        while (index > 0 && temp > heapArray[getParentIndex(index)]) {
            heapArray[index] = heapArray[getParentIndex(index)];
            index = getParentIndex(index);
        }
        heapArray[index] = temp;
    }

    public int popMax() {
        int maxItem = heapArray[0];
        heapArray[0] = heapArray[size - 1];
        heapArray[size - 1] = -1;
        size--;

        int index = 0;
        while (index < size - 1) {
            heapifyUp(index);
            index++;
        }

        return maxItem;
    }

    public void print() {
        for (int i = 0; i < size; i++) {
            System.out.print(heapArray[i]);
            System.out.print(',');
        }
        System.out.println();
    }

    public static void main(String[] args) {
        double power = 2; // Example value for the power
        int capacity = 10; // Example capacity

        PowerHeap heap = new PowerHeap(power, capacity);
        heap.insert(5);
        heap.insert(10);
        heap.insert(3);

        heap.print();

        int maxItem = heap.popMax();
        System.out.println("Max item: " + maxItem);

        heap.print();
    }
}
