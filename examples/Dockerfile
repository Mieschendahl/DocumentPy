# Use the official Python base image
FROM python:3.13-slim

# Install bash
RUN apt-get update && apt-get install -y bash git vim

# Installs requirements
RUN pip install --upgrade pip && pip install --upgrade git+https://github.com/Mieschendahl/DocumentPy.git

# Create a new user and group
RUN useradd -m user

# Switch to the new user
USER user

# Set work dir
WORKDIR /home/user/documentpy/examples

# Copy files
COPY --chown=user:user ./examples/example_* ./examples/code_* ./

# Start an interactive bash shell by default
CMD ["bash"]