# Data Visualization with Python (IBM)

This repository contains a Dash application for data visualization with Python, as well as [static analysis Jupyter notebook](static_analysis.ipynb) with some beautiful [plots](plots/), like:

![Automobile Sales Over Years](plots/Line_Plot_1.png)
![Estimation of ad Expenditure](plots/Pie_1.png)
## Usage of the Dash app

### Clone the Repository

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/andreypomortsev/data-visualization-with-python-IBM.git
```

### Change the directory to the repository:

```bash
cd data-visualization-with-python-IBM
```

### Build and Run the Docker Container

To build a Docker container and run the Dash application:

1. Build the Docker image from the repository's root directory:
   ```bash
   docker build -t your-image-name .
   ```
   Replace `your-image-name` with a suitable name for your Docker image.

2. Run the Docker container based on the built image, mapping port `8080` of the container to port `8080` on the host machine:
   ```bash
   docker run -p 8080:8080 your-image-name
   ```
   Replace `your-image-name` with the name you specified when building the Docker image.

## Contributing

Feel free to contribute to this project by submitting pull requests or raising issues.

## License

This project is licensed under the [MIT License](LICENSE).
