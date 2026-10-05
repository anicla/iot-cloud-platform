FROM httpd:2.4
COPY ./code /usr/local/apache2/htdocs/
COPY entrypoint.sh /usr/local/bin/frontend-entrypoint.sh
RUN chmod +x /usr/local/bin/frontend-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/frontend-entrypoint.sh"]
CMD ["httpd-foreground"]
