import pandas as pd
import matplotlib.pyplot as plt


def main():
    data_test0 = pd.read_csv('./signal_data/reference/ref_signal0.csv')
    plt.plot(data_test0['Time'], data_test0['Intensity'], label='Reference Signal 0')
    data_test1 = pd.read_csv('./signal_data/reference/ref_signal1.csv')
    plt.plot(data_test1['Time'], data_test1['Intensity'], label='Reference Signal 1')
    data_test2 = pd.read_csv('./signal_data/reference/ref_signal2.csv')
    plt.plot(data_test2['Time'], data_test2['Intensity'], label='Reference Signal 2')
    data_test3 = pd.read_csv('./signal_data/reference/ref_signal3.csv')
    plt.plot(data_test3['Time'], data_test3['Intensity'], label='Reference Signal 3')
    plt.xlabel('Time')
    plt.ylabel('Intensity')
    plt.title('Reference Signals')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()