# IAQ systemd service files

## !! Info
Before copying and enabling the service files you will need to change the directory paths and the username `vuj` to your own directory and username.

## Copying systemd files into `/etc/systemd/system/`
The command below copies the service files in this directory into `/etc/systemd/system/`.
```
sudo cp -r iaq-* /etc/systemd/system/.
```

## Enabling and running services
The command below will enable the services on boot and start them now.
```
sudo systemctl enable --now iaq*.service
```

## Checking if services are running
The command below will help you check if the services are running.

### Checking on backend
```
sudo systemctl status iaq-backend.service
```

### Checking on frontend
```
sudo systemctl status iaq-frontend.service
```