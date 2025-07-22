# Use an official Ubuntu as a parent image
FROM idaholab/moose-dev:latest

# Set environment variables to non-interactive (for apt-get)
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory
WORKDIR /home

# Copy the current directory contents into the container at /app
COPY . /home/ThermalElasticToolkit

# (Optional) Install Python dependencies if requirements.txt exists
RUN pip3 install --no-cache-dir \
    meshio \
    numpy \
    matplotlib \
    scipy

RUN git clone https://github.com/finalbossqc/moose.git /home/moose

# Set the default command to bash
CMD ["/bin/bash"]
