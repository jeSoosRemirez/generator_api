### Before the start
When the instance is just started or restarted the IP probably has changed.
So the IP(server_name) should be changed here "/etc/nginx/sites-enabled/fastapi_nginx".

To do that run:

    $ sudo vim /etc/nginx/sites-enabled/fastapi_nginx
    Type "i" to enter insert mode in VIM, change the IP just after "server_name" to the new IP,
    press Esc and type :wq! to save and exit file.

    Then restart nginx
    $ sudo service nginx restart

!!! If the instance hasn't been turned off then the IP stills static and you don't need to change nginx config.

### How to start
To start API:

    $ cd generator_api/
    $ uvicorn main:app

### How to use
"https" should be changed to "http" then provide IPv4 that you can find in the instances tab on AWS site.
Example: http://16.171.136.10/

Endpoints:

    UI:
    /docs

    Generate image and get the url of it:
    /get_generated_image/{image_name}
    Also, "additional_prompt" can be povided

    Examples:
    http://13.51.150.31/docs
    http://13.51.150.31/get_generated_image/pierogi
    http://13.51.150.31/get_generated_image/pierogi?additional_prompt=%20painted%20in%20pink%20color

### To do
- Have preloaded model
- Create queue for generation
- Rework Stable diffusion to not start the script through terminal