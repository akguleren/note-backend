#!/bin/bash

# Docker Deployment Script for Notes API
# This script helps you deploy the Notes API using Docker

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker is not running. Please start Docker."
        exit 1
    fi
    
    print_success "Docker is installed and running"
}

# Function to check if .env file exists
check_env_file() {
    if [ ! -f .env ]; then
        print_warning ".env file not found"
        if [ -f .env.example ]; then
            print_status "Copying .env.example to .env"
            cp .env.example .env
            print_warning "Please edit .env file with your Firebase credentials before continuing"
            read -p "Press enter when you've configured .env file..."
        else
            print_error "No .env.example file found. Please create .env file with your configuration"
            exit 1
        fi
    else
        print_success ".env file found"
    fi
}

# Function to build Docker image
build_image() {
    print_status "Building Docker image..."
    docker build -t notes-api:latest .
    print_success "Docker image built successfully"
}

# Function to stop existing container if running
stop_existing_container() {
    if docker ps | grep -q notes-api-container; then
        print_status "Stopping existing container..."
        docker stop notes-api-container
        docker rm notes-api-container
        print_success "Existing container stopped and removed"
    fi
}

# Function to run the container
run_container() {
    print_status "Starting new container..."
    docker run -d \
        --name notes-api-container \
        --env-file .env \
        -p 8000:8000 \
        --restart unless-stopped \
        notes-api:latest
    
    print_success "Container started successfully"
    print_status "Container name: notes-api-container"
    print_status "Port: 8000"
    print_status "API URL: http://localhost:8000"
}

# Function to check if container is healthy
check_health() {
    print_status "Waiting for container to start..."
    sleep 5
    
    for i in {1..12}; do
        if curl -f http://localhost:8000 &> /dev/null; then
            print_success "API is responding! 🎉"
            print_status "API Documentation: http://localhost:8000/docs"
            return 0
        fi
        print_status "Waiting for API to start... ($i/12)"
        sleep 5
    done
    
    print_error "API did not start properly. Check logs with: docker logs notes-api-container"
    return 1
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy     - Build and deploy the application (default)"
    echo "  build      - Only build the Docker image"
    echo "  start      - Start the container (assumes image exists)"
    echo "  stop       - Stop the container"
    echo "  logs       - Show container logs"
    echo "  status     - Show container status"
    echo "  restart    - Restart the container"
    echo "  clean      - Stop container and remove image"
    echo "  help       - Show this help message"
}

# Function to show logs
show_logs() {
    if docker ps | grep -q notes-api-container; then
        print_status "Showing container logs (Ctrl+C to exit)..."
        docker logs -f notes-api-container
    else
        print_error "Container is not running"
    fi
}

# Function to show status
show_status() {
    print_status "Container status:"
    if docker ps | grep -q notes-api-container; then
        docker ps | grep notes-api-container
        echo ""
        print_status "Container stats:"
        docker stats notes-api-container --no-stream
    else
        print_warning "Container is not running"
        if docker ps -a | grep -q notes-api-container; then
            print_status "Stopped container found:"
            docker ps -a | grep notes-api-container
        fi
    fi
}

# Function to restart container
restart_container() {
    if docker ps | grep -q notes-api-container; then
        print_status "Restarting container..."
        docker restart notes-api-container
        print_success "Container restarted"
        check_health
    else
        print_error "Container is not running"
    fi
}

# Function to clean up
clean_up() {
    print_status "Cleaning up..."
    
    # Stop and remove container
    if docker ps | grep -q notes-api-container; then
        docker stop notes-api-container
    fi
    
    if docker ps -a | grep -q notes-api-container; then
        docker rm notes-api-container
    fi
    
    # Remove image
    if docker images | grep -q notes-api; then
        docker rmi notes-api:latest
    fi
    
    print_success "Cleanup completed"
}

# Main deployment function
deploy() {
    print_status "Starting deployment process..."
    check_docker
    check_env_file
    stop_existing_container
    build_image
    run_container
    check_health
    
    echo ""
    print_success "🚀 Deployment completed successfully!"
    echo ""
    echo "Quick commands:"
    echo "  View logs: docker logs -f notes-api-container"
    echo "  Stop: docker stop notes-api-container"
    echo "  Restart: docker restart notes-api-container"
    echo ""
    echo "API Endpoints:"
    echo "  • Main: http://localhost:8000"
    echo "  • Docs: http://localhost:8000/docs"
    echo "  • ReDoc: http://localhost:8000/redoc"
}

# Parse command line arguments
case "${1:-deploy}" in
    "deploy")
        deploy
        ;;
    "build")
        check_docker
        build_image
        ;;
    "start")
        check_docker
        run_container
        check_health
        ;;
    "stop")
        if docker ps | grep -q notes-api-container; then
            docker stop notes-api-container
            print_success "Container stopped"
        else
            print_warning "Container is not running"
        fi
        ;;
    "logs")
        show_logs
        ;;
    "status")
        show_status
        ;;
    "restart")
        restart_container
        ;;
    "clean")
        clean_up
        ;;
    "help"|"-h"|"--help")
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        show_usage
        exit 1
        ;;
esac
