import displayio
from adafruit_display_shapes.rect import Rect
from utils import *
import time

class Sort:
    def __init__(self, display, w, h):
        self.display = display
        self.color = 0xFFFFFF
        self.WIDTH = w
        self.HEIGHT = h
        self.column_width = 2
        self.num_of_columns = self.WIDTH // self.column_width
        self.columns = []
        for i in range(min(self.num_of_columns, self.HEIGHT)):
            height = i + 1
            self.columns.append(
                Rect(
                    x=i * self.column_width,
                    y=self.HEIGHT - i - 1,
                    width=2,
                    height=height,
                    fill=self.color,
                )
            )
        array_shuffle(self.columns)
        self.repair()

    def repair(self):
        for i in range(min(self.num_of_columns, self.HEIGHT)):
            self.columns[i].x = i * self.column_width

    def reset(self):
        for rect in self.columns:
            rect.x = (rect.height-1) * self.column_width
        array_shuffle(self.columns)

    def show(self):
        self.group = displayio.Group()
        self.display.root_group = self.group
        for col in self.columns:
            self.group.append(col)

        while True:
            self.mergeSort(self.columns, 0, len(self.columns)-1)
            self.reset()
            self.repair()
            self.quickSort(self.columns, 0, len(self.columns)-1)
            self.reset()
            self.repair()
            self.insertionSort(self.columns)
            self.reset()
            self.repair()
            self.selectionSort(self.columns)
            self.reset()
            self.repair()
            self.bubbleSort(self.columns)
            self.reset()
            self.repair()

    def merge(self, arr, left, mid, right):
        delay = 0.4
        clr_selected_1 = 0x00ff00
        clr_selected_2 = 0xff0000
        clr_pivot = 0x00ffff
        clr_sorted = 0x0000ff
        clr_range = 0xff00ff
        # Inicjalizacja wskaźników
        start1 = left
        start2 = mid + 1

        for i in range(left, mid+1):
            arr[i].fill = clr_range

        for i in range(mid+1, right+1):
            arr[i].fill = clr_pivot

        time.sleep(delay*2)

        # Jeżeli podtablice są już posortowane, to nic nie trzeba robić
        if arr[mid].height <= arr[start2].height:
            return

        # Scalanie dwóch podtablic
        while start1 <= mid and start2 <= right:
            # Jeżeli element w pierwszej podtablicy jest na właściwej pozycji
            if arr[start1].height <= arr[start2].height:
                start1 += 1
            else:
                # Element w drugiej podtablicy jest mniejszy, trzeba go przesunąć
                value = arr[start2]
                index = start2

                # Przesunięcie wszystkich elementów pomiędzy start1 a start2 w prawo o jedno miejsce
                while index != start1:
                    arr[index] = arr[index - 1]
                    index -= 1
                    self.repair()
                    time.sleep(delay*2)
                arr[start1] = value
                self.repair()
                time.sleep(delay*2)
                # Aktualizacja wskaźników
                start1 += 1
                mid += 1
                start2 += 1
        for i in range(left, mid+1):
            arr[i].fill = self.color

        for i in range(mid+1, right+1):
            arr[i].fill = self.color

    def mergeSort(self, arr, left, right):
        if left < right:
            mid = (left + right) // 2

            self.mergeSort(arr, left, mid)
            self.mergeSort(arr, mid + 1, right)
            self.merge(arr, left, mid, right)

    def partition(self, arr, l, r):
        delay = 0.4
        clr_selected_1 = 0x00ff00
        clr_selected_2 = 0xff0000
        clr_pivot = 0x00ffff
        clr_sorted = 0x0000ff
        clr_range = 0xff00ff
        time.sleep(delay*2)
        i = l - 1

        #color range l -> r

        for j in range(l, r+1):
            arr[j].fill = clr_range

        time.sleep(delay*2)

        pivot = arr[r].height
        arr[r].fill = clr_pivot
        time.sleep(delay*2)

        for j in range(l, r):
            arr[j].fill = clr_pivot
            time.sleep(delay)
            if arr[j].height < pivot:
                arr[j].fill = clr_selected_1
                time.sleep(delay)
                i += 1
                if j != i:
                    arr[i].fill = clr_selected_2
                time.sleep(delay*2)
                arr[i].x, arr[j].x = arr[j].x, arr[i].x
                arr[i], arr[j] = arr[j], arr[i]
            else:
                arr[j].fill = clr_selected_2
            time.sleep(delay*2)
            if j != i:
                arr[j].fill = self.color
            else:
                arr[j].fill = clr_selected_1
        if i + 1 != r:
            arr[i + 1].fill = clr_selected_2
            time.sleep(delay*3)
            arr[i + 1].x, arr[r].x = arr[r].x, arr[i + 1].x
            arr[i + 1], arr[r] = arr[r], arr[i + 1]
            time.sleep(delay*3)
        arr[i + 1].fill = clr_sorted
        if r != i+1:
            arr[r].fill = self.color
        time.sleep(delay*3)
        for j in range(l, i + 1):
            arr[j].fill = self.color

        return i + 1

    def quickSort(self, arr, l, r):
        if l <= r:
            pi = self.partition(arr, l, r)

            self.quickSort(arr, l, pi - 1)
            self.quickSort(arr, pi + 1, r)

    def insertionSort(self, arr):
        delay = 0.4
        clr_selected_1 = 0x00ff00
        clr_selected_2 = 0xff0000
        clr_sorted = 0x0000ff
        # Function to sort array using insertion sort
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            key.fill = clr_selected_1
            time.sleep(delay)
            # Move elements of arr[0..i-1], that are
            # greater than key, to one position ahead
            # of their current position
            swaped = False
            while j >= 0 and key.height < arr[j].height:
                arr[j].fill = clr_selected_2
                swaped = True
                time.sleep(delay)
                arr[j].x += 2
                time.sleep(delay)
                arr[j + 1] = arr[j]
                arr[j].fill = self.color
                j -= 1
            time.sleep(delay*2)
            if swaped:
                key.x = arr[j + 1].x - 2
                arr[j + 1] = key
            time.sleep(delay*2)
            key.fill = self.color

    def selectionSort(self, array):
        delay = 0.4
        clr_selected_1 = 0x00ff00
        clr_selected_2 = 0xff0000
        clr_sorted = 0x0000ff
        size = len(array)
        for step in range(size):
            min_idx = step
            array[min_idx].fill = clr_selected_1

            for i in range(step + 1, size):
                array[i].fill = clr_selected_1
                time.sleep(delay)
                # to sort in descending order, change > to < in this line
                # select the minimum element in each loop
                if array[i].height < array[min_idx].height:
                    array[min_idx].fill = clr_selected_2
                    time.sleep(delay)
                    array[min_idx].fill = self.color
                    min_idx = i
                else:
                    array[i].fill = clr_selected_2
                    time.sleep(delay)
                    array[i].fill = self.color
            array[step].fill = clr_selected_1
            time.sleep(delay*3)
            # put min at the correct position
            array[step], array[min_idx] = array[min_idx], array[step]
            array[step].x, array[min_idx].x = array[min_idx].x, array[step].x
            time.sleep(delay*3)
            array[step].fill = clr_sorted
            if step != min_idx:
                array[min_idx].fill = self.color

    def bubbleSort(self, array):
        delay = 0.4
        clr_selected_1 = 0x00ff00
        clr_selected_2 = 0xff0000
        clr_sorted = 0x0000ff
        # loop to access each array element
        for i in range(len(array)):

            # loop to compare array elements
            for j in range(0, len(array) - i - 1):

                # compare two adjacent elements
                # change > to < to sort in descending order
                array[j].fill = clr_selected_1
                array[j+1].fill = clr_selected_1
                time.sleep(delay)
                if array[j].height > array[j + 1].height:
                    array[j].fill = clr_selected_2
                    time.sleep(delay)
                    array[j], array[j + 1] = array[j + 1], array[j]
                    array[j].x, array[j + 1].x = array[j + 1].x, array[j].x
                else:
                    array[j+1].fill = clr_selected_2
                time.sleep(delay)
                array[j].fill = self.color
                array[j+1].fill = self.color
            array[len(array) - i - 1].fill = clr_sorted
