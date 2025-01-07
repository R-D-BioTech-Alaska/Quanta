# Quanta
Quantum Calculator for understanding variables and outcomes

---

**Quanta** is a Python-based Quantum Calculator with a graphical user interface (GUI) built using Tkinter. It enables users to perform various quantum computations, including observing qubits, calculating error rates, applying quantum gates, calculating spin, and running Grover's algorithm. Useful for building programs that require understanding gates, states and different aspects of running qubits for software or hardware quantum systems.

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Settings](#settings)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Observe Qubits**: Measure a specified number of qubits and view the results.
- **Calculate Error Rates**: Determine the error rate based on qubit measurements.
- **Apply Quantum Gates**: Apply various quantum gates (RX, RY, RZ, H, X) to selected qubits.
- **Calculate Spin**: Compute the spin of a qubit based on its state.
- **Grover's Algorithm**: Run Grover's algorithm to analyze quantum search speed.
- **Real-time Logs**: Monitor application logs within the GUI and access detailed logs in the `quantum_verse_calculator.log` file.


## Installation

### Prerequisites

- **Python 3.11**: Ensure you have Python 3.11 installed. You can download it from the [official website](https://www.python.org/downloads/).
- **pip**: Python's package installer should be available with your Python installation.

### Clone the Repository

```bash
git clone https://github.com/R-D-BioTech-Alaska/Quanta.git
cd Quanta
```

### Install Dependencies

Quanta relies on several Python packages. It's recommended to use a virtual environment to manage dependencies.

1. **Create a Virtual Environment**

    ```bash
    python3.11 -m venv venv
    ```

2. **Activate the Virtual Environment**

    - **Windows:**

        ```bash
        venv\Scripts\activate
        ```

    - **macOS/Linux:**

        ```bash
        source venv/bin/activate
        ```

3. **Install Required Packages**

    ```bash
    pip install -r requirements.txt
    ```

    *If `requirements.txt` is not provided, install the necessary packages manually:*

    ```bash
    pip install qiskit qiskit-aer
    ```

    *Tkinter is included with standard Python installations. If it's missing, refer to your operating system's instructions to install it.*

## Usage

Run the Quanta application using the following command:

```bash
python Quanta.py
```

### Application Tabs

1. **Observe Qubits**
    - **Number of Qubits**: Specify how many qubits you want to observe.
    - **Shots**: Define the number of measurement shots.
    - **Observe Button**: Execute the observation and view results in the output section.

2. **Error Rates**
    - **Number of Qubits**: Specify the qubits involved.
    - **Shots**: Define the number of measurement shots.
    - **Calculate Error Rate Button**: Compute and display the error rate.

3. **Gate Variables**
    - **Gate Type**: Select the type of quantum gate to apply (RX, RY, RZ, H, X).
    - **Angle**: Specify the angle for rotation gates (RX, RY, RZ).
    - **Qubit Index**: Choose the qubit to which the gate will be applied.
    - **Apply Gate Button**: Execute the gate application and view the state vector and measurement results.

4. **Calculate Spin**
    - **Qubit State**: Select the state of the qubit (0 or 1).
    - **Calculate Spin Button**: Compute and display the spin based on the qubit state.

5. **Grover's Speed**
    - **Target State (binary)**: Input the target state in binary.
    - **Number of Qubits**: Specify the number of qubits for Grover's algorithm.
    - **Run Grover's Algorithm Button**: Execute the algorithm and view the speed.

6. **Settings**
    - **Font Size**: Adjust the font size for better readability.
    - **Theme**: Switch between Dark and Light themes to suit your preference.
    - **Apply Settings Button**: Apply the selected settings immediately.

### Logs

Monitor real-time logs within the application under the **Logs** section. Detailed logs are also saved in the `quantum_verse_calculator.log` file located in the project's root directory.

## Settings

Customize your Quanta experience through the **Settings** tab:

- **Font Size**: Use the spinbox to select your desired font size (ranging from 8 to 20).
- **Theme**: Choose between Dark and Light themes to enhance visibility and reduce eye strain.
- **Apply Settings**: Click the button to apply your chosen settings instantly.

## Contributing

Contributions are welcome! To contribute to Quanta, please follow these steps:

1. **Fork the Repository**

    Click the "Fork" button at the top right of the repository page.

2. **Create a New Branch**

    ```bash
    git checkout -b feature/YourFeatureName
    ```

3. **Commit Your Changes**

    ```bash
    git commit -m "Add feature: YourFeatureName"
    ```

4. **Push to the Branch**

    ```bash
    git push origin feature/YourFeatureName
    ```

5. **Create a Pull Request**

    Navigate to the original repository and click "Compare & pull request." Provide a clear description of your changes and submit the pull request.

## License

This project is licensed under the [MIT License](https://github.com/R-D-BioTech-Alaska/Quanta/blob/main/LICENSE). See the [LICENSE](LICENSE) file for details.

- **GitHub**: [@R-D-BioTech-Alaska](https://github.com/R-D-BioTech-Alaska)
- **Website**: [R&D BioTech Alaska](http://www.rdbiotech.org)

---
