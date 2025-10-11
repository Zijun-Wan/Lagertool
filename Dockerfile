# Use official OpenJDK image
FROM openjdk:17-jdk-slim

# Set working directory
WORKDIR /app

# Copy your JAR file into the container
COPY Lagertool.jar ./

# Expose port (change if your app uses a different port)
EXPOSE 8080

# Run the JAR file
CMD ["java", "-jar", "Lagertool.jar"]