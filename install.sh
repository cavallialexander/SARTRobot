#!/bin/bash

# SIGHTS installer
# Handles installing and updating SIGHTS
# 
# Created by the Semi-Autonomous Rescue Team
# This file is part of the SIGHTS project
#
# https://www.sights.dev/
# https://www.github.com/sightsdev


INSTALL_DIR=/opt
MOTION_VER=4.3.2

update_only='false'
developer_versions='false'
internal_update='false'

apt_updated='false'

set -e

print_detected_ip () {
  output="Visit http://localhost$1 on the host machine"
  hostname=$(hostname -I)
  if [[ $hostname ]]
  then
    for ip in $hostname
    do
      output="$output or http://$ip$1"
    done
    output="$output on any device on the local network."
  else
    output="$output or connect to a network."
  fi
  echo "$output"
  echo
}

enable_ssh () {
    echo -e "\nEnabling SSH..."
    systemctl enable ssh
    echo -e "\nStarting SSH..."
    systemctl start ssh
}

install_dependencies () {
    echo -e "\nInstalling dependencies..."
    apt update
    apt install -y git apache2 python3 python3-pip wget gdebi 
    apt_updated='true'
    echo
}

checkout_release () {
  # Check out the latest tag (latest versioned release) for each repository.
  # Skip if developer versions are enabled (meaning master will be checked out)
  if [ $developer_versions == 'false' ]
  then
    cd sights
    git checkout -f sart_2024
    git checkout `git tag | sort -V | tail -1`
    cd ..
  fi
}

install_sights_repositories () {
    echo -e "\nDownloading SIGHTS repositories..."

    # Get SIGHTS
    git clone https://github.com/sightsdev/sights

    # Checkout to latest stable release
    checkout_release

    # Install all Python packages required by SIGHTS
    echo -e "\nInstalling required Python packages..."
    python3 -m pip install -r sights/src/requirements.txt
    echo
}

configure_apache () {
    echo -e "\nSetting up Apache..."

    # This is the site file that defines where the interface is hosted from
    # It also sets up a reverse proxy for Supervisor to work correctly
    echo -e "\nEnabling SIGHTS site config..."
    ln -sf $INSTALL_DIR/sights/src/configs/apache/sights.conf /etc/apache2/sites-enabled/sights.conf

    # This is the required option to allow Apache to host from $INSTALL_DIR
    echo -e "\nAllowing Apache to host the interface directory..."
    # Only append this to the file if it does not already exist
    if grep -Fxq "<Directory ${INSTALL_DIR}/>" /etc/apache2/apache2.conf
    then
        echo -e "Already done..."
    else
        echo -e "<Directory ${INSTALL_DIR}/>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>" >> /etc/apache2/apache2.conf
    fi

    echo -e "\nDisabling Apache default site..."
    a2dissite 000-default.conf

    echo -e "\nEnabling Apache proxy modules..."
    a2enmod proxy
    a2enmod proxy_http

    echo -e "\nStarting Apache..."
    service apache2 restart
    service apache2 start
    service apache2 reload
    echo
    print_detected_ip "/"
}

try_install_motion () {
    echo -e "\nWould you like to attempt to install a prebuilt Motion package?"
    echo -e "Currently only available on Raspberry Pi and x64-based platforms."
    echo -e "NOTE: This option is not available for the Jetson Nano"

    echo -e "\nOtherwise a manual install will be performed.\n"

    read -p "Attempt to install a prebuilt package Motion? [y/n] " choice
        case "$choice" in 
        y|Y ) install_motion_auto;;
        n|N ) install_motion_manual;;
        * ) echo "Invalid response";;
    esac
}

install_motion_auto () {
    # Only install prebuilt binaries which are available only on supported OSs
    if [ $DETECTED_OS == "ubuntu" ] || [ $DETECTED_OS == "debian" ] || [ $DETECTED_OS == "raspbian" ]
    then
        if [ $DETECTED_CODENAME == "bionic" ] || [ $DETECTED_CODENAME == "cosmic" ] || [ $DETECTED_CODENAME == "buster" ] || [ $DETECTED_CODENAME == "focal" ]
        then
            echo -e "\nDownloading Motion..."
            
            if [ $DETECTED_OS == "raspbian" ]
            then 
                # Get the armhf binaries (with the pi prefix) for Raspbian
                wget https://github.com/Motion-Project/motion/releases/download/release-${MOTION_VER}/pi_${DETECTED_CODENAME}_motion_${MOTION_VER}-1_armhf.deb -O motion.deb
            else
                # For x86 systems, just use the normal amd64 binaries
                wget https://github.com/Motion-Project/motion/releases/download/release-${MOTION_VER}/${DETECTED_CODENAME}_motion_${MOTION_VER}-1_amd64.deb -O motion.deb
            fi

            echo -e "\nInstalling Motion..."
            gdebi -n ./motion.deb
            rm ./motion.deb

            configure_motion
        else
            echo -e "\nUnsupported release"
        fi
    else
        echo -e "\nUnsupported distribution"
    fi
    echo
    print_detected_ip ":8080/"
}

install_motion_manual () {
    cd /tmp/

    echo -e "\nDownloading build script..."
    wget https://raw.githubusercontent.com/Motion-Project/motion-packaging/master/builddeb.sh
    chmod +x builddeb.sh

    echo -e "\nBuilding Motion..."
    ./builddeb.sh AdhocBuild AdhocBuild@nowhere.com master y any
    rm builddeb.sh

    echo -e "\nInstalling Motion..."
    gdebi -n *motion*.deb
    rm *motion*.deb

    cd $INSTALL_DIR

    configure_motion
}

configure_motion () {
    echo -e "\nCreating symlink for Motion configuration files..."
    rm -r /etc/motion
    ln -sf $INSTALL_DIR/sights/src/configs/motion /etc

    echo -e "\nEnabling Motion daemon flag..."
    echo "start_motion_daemon=yes" > /etc/default/motion

    echo -e "\nEnabling Motion service..."
    systemctl enable motion

    echo -e "\nStarting Motion service..."
    service motion start
    service motion restart
}

install_shellinabox () {
    echo -e "\nInstalling ShellInABox..."
    if [ $apt_updated == 'false' ]; then
        apt update
        apt_updated='true'
    fi
    apt install -y shellinabox

    echo -e "\nDisabling ShellInABox SSL..."
    sed -i 's/SHELLINABOX_ARGS=.*/SHELLINABOX_ARGS="--no-beep --disable-ssl"/' /etc/default/shellinabox

    if [ $DETECTED_OS == "raspbian" ]; then
        enable_ssh
    fi

    echo -e "\nStarting shellinabox service..."
    service shellinabox start
    echo
    print_detected_ip ":4200/"
}

configure_supervisor () {
    echo -e "\nCreating symlink for Supervisor configuration files..."
    ln -sf $INSTALL_DIR/sights/src/configs/supervisor /etc

    echo -e "\nInstalling Supervisor SIGHTS extension..."
    python3 -m pip install sights/src/supervisor_plugin

    echo -e "\nInstalling Supervisor init script"
    cp sights/src/configs/systemd/supervisord /etc/init.d/
    chmod 755 /etc/init.d/supervisord
    chown root:root /etc/init.d/supervisord
    update-rc.d supervisord defaults

    echo -e "\nRunning Supervisor"
    /etc/init.d/supervisord start
    
    echo
    print_detected_ip ":9001/"
}

enable_i2c () {
    if [ $DETECTED_OS == "raspbian" ]
    then 
        echo -e '\nEnabling i2c-bcm2708 module...'
        if grep -q 'i2c-bcm2708' /etc/modules; then
            echo 'i2c-bcm2708 module already enabled.'
        else
            modprobe i2c-bcm2708
            echo 'i2c-bcm2708' >> /etc/modules
            echo -e '\nEnabled i2c-bcm2708 module.'
        fi

        echo -e '\nEnabling i2c-dev module...'
        if grep -q 'i2c-dev' /etc/modules; then
            echo -e 'i2c-dev module already enabled.'
        else
            modprobe i2c-dev
            echo 'i2c-dev' >> /etc/modules
            echo -e 'Enabled i2c-dev module.'
        fi

        echo -e '\nSetting i2c_arm parameter boot config option...'
        if grep -q 'dtparam=i2c_arm=on' /boot/config.txt; then
            echo -e 'i2c_arm parameter already set.'
        else
            echo 'dtparam=i2c_arm=on' >> /boot/config.txt
            echo -e '\nSet i2c_arm parameter boot config option...'
        fi

        echo -e '\nRemoving i2c from blacklists...'
        if [ -f /etc/modprobe.d/raspi-blacklist.conf ]; then
            sed -i 's/^blacklist spi-bcm2708/#blacklist spi-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
            sed -i 's/^blacklist i2c-bcm2708/#blacklist i2c-bcm2708/' /etc/modprobe.d/raspi-blacklist.conf
        else
            echo 'File raspi-blacklist.conf does not exist, skip this step.'
        fi
    else
        echo -e '\nThis option can only be used on a Raspberry Pi (running Raspbian).'
        echo -e '\nFor other devices or operating systems, consult the manufacturers documentation for enabling I2C.'
    fi

}

update () {
    echo -e "\nUpdating SIGHTS..."

    cd sights
    git checkout -f sart_2024
    git pull
    cd $INSTALL_DIR

    # Checkout appropriate release (stable or dev)
    checkout_release

    # Update Supervisor 
    python3 -m pip install sights/src/supervisor_plugin

    # Ensure up to date dependencies are installed
    python3 -m pip install -r sights/src/requirements.txt

    # If update flag specified, just update, then exit
    if [ $internal_update == 'false' ]; then
        echo -e "\nRestarting Supervisord and SIGHTS..."
        service supervisord restart
    fi
    
    echo -e "\nUpdate complete!"
    echo
    print_detected_ip "/"
}

complete_install () { 
    install_dependencies
    install_sights_repositories
    configure_apache
    try_install_motion
    install_shellinabox
    configure_supervisor
    echo -e "\nInstallation complete! Reboot to ensure proper functionality."
    print_detected_ip "/"
}

# Ensure user is running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Setup install directory
if [ ! -d "$INSTALL_DIR" ]; then
    echo -e "Creating installation directory at $INSTALL_DIR"
    mkdir $INSTALL_DIR
fi

# Go to directory
cd $INSTALL_DIR

# Print welcome message
echo "  _____ _____ _____ _    _ _______ _____ "
echo " / ____|_   _/ ____| |  | |__   __/ ____|"
echo "| (___   | || |  __| |__| |  | | | (___  "
echo " \___ \  | || | |_ |  __  |  | |  \___ \ "
echo " ____) |_| || |__| | |  | |  | |  ____) |"
echo "|_____/|_____\_____|_|  |_|  |_| |_____/ "

echo -e "\nSights interactive installer"
echo -e "Created by the Semi-Autonomous Rescue Team"

DETECTED_OS=$(cat /etc/*-release | grep -E "\bID=" | sed 's/ID=//g')
DETECTED_CODENAME=$(cat /etc/*-release | grep "VERSION_CODENAME" | sed 's/VERSION_CODENAME=//g')

echo -e "\nInstalling as: $SUDO_USER"
echo -e "Detected OS: ${DETECTED_OS^} ${DETECTED_CODENAME^}"
if [ $DETECTED_OS == "ubuntu" ] || [ $DETECTED_OS == "debian" ] || [ $DETECTED_OS == "raspbian" ]
then
    echo -e "- Using a supported OS -"
else
    echo -e "- Using an unsupported OS -"
fi
echo

# Check provided flags
while test $# -gt 0; do
        case "$1" in
            --update)
                update_only='true'
                shift
                ;;
            --dev)
                developer_versions='true'
                shift
                ;;
            --internal)
                internal_update='true'
                shift
                ;;
            *)
               echo "$1 is not a recognized flag!"
               exit 1
               ;;
        esac
  done

# If developer versions flag specified, notify and continue
if [ $developer_versions == 'true' ]; then
    echo -e "Developer versions will be used."
fi

# If update flag specified, just update, then exit
if [ $update_only == 'true' ]; then
    echo -e "Performing an update..."
    update
    exit 0
fi

options=(
    "Complete Install" 
    "Install Dependencies" 
    "Install SIGHTS Software"
    "Configure Apache" 
    "Install Motion" 
    "Setup ShellInABox" 
    "Configure Supervisor"
    "Enable I2C"
    "Update"
    "Detect IPs"
)
PS3="Enter a number (1-${#options[@]}) or q to quit: "

while true; do
  select option in "${options[@]}"; do
    case "$REPLY" in
        1) complete_install ;;
        2) install_dependencies ;;
        3) install_sights_repositories ;;
        4) configure_apache ;;
        5) try_install_motion ;;
        6) install_shellinabox ;;
        7) configure_supervisor ;;
        8) enable_i2c ;;
        9) update ;;
        10) print_detected_ip "/" ;;
        q) exit ;;
    esac
    break
  done
done
