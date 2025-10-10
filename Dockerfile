# Use base image: PHP-FPM, version 7.4.16
FROM php:7.4.16-fpm
 
# Install basic apt packages
RUN apt-get update && apt-get install -y apt-utils unzip gnupg2 libpng-dev zlib1g-dev
 
# Download and install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
 
# Install & enable bcmath, pcntl, gd PHP extensions
RUN docker-php-ext-install bcmath pcntl gd
 
# Install PECL extensions and enable them
RUN pecl install xdebug
RUN docker-php-ext-enable xdebug