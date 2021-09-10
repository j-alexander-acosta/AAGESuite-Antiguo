FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf


# RUN wget https://s3.amazonaws.com/shopify-managemant-app/wkhtmltopdf-0.9.9-static-amd64.tar.bz2
# RUN tar xvjf wkhtmltopdf-0.9.9-static-amd64.tar.bz2
# RUN mv wkhtmltopdf-amd64 /usr/local/bin/wkhtmltopdf
# RUN chmod +x /usr/local/bin/wkhtmltopdf

# unixodbc 2.3.7
# RUN wget ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.7.tar.gz
# RUN tar -xzf unixODBC-2.3.7.tar.gz
# RUN cd unixODBC-2.3.7 && \
#    ./configure --prefix=/usr \
#    --sysconfdir=/etc/unixODBC && make && make install
# RUN rm unixODBC-2.3.7.tar.gz


# freetds 1.00.97
# RUN wget ftp://ftp.freetds.org/pub/freetds/stable/freetds-1.00.97.tar.gz
# RUN tar -xzf freetds-1.00.97.tar.gz
# RUN cd freetds-1.00.97 && ./configure --prefix=/usr/local --with-tdsver=7.4 \
#     && make && make install
# RUN  rm freetds-1.00.97.tar.gz


WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/