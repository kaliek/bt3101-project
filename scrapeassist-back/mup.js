module.exports = {
  servers: {
    one: {
      host: '115.66.242.122',
      username: 'root',
    }
  },

  app: {
    // TODO: change app name and path
    name: 'bt3101',
    path: '.',
    volumes: {
      '/etc/timezone':'/etc/timezone',
      '/etc/localtime':'/etc/localtime',
      '/usr/share/zoneinfo':'/usr/share/zoneinfo'
    },

    servers: {
      one: {},
    },

    buildOptions: {
      serverOnly: true,
    },

    env: {
      // TODO: Change to your app's url
      // If you are using ssl, it needs to start with https://
      ROOT_URL: 'http://bt3101-backend',
      MONGO_URL: 'mongodb://115.66.242.122:9212/bt3101',
      PORT: 3100,
      TZ: "Asia/Singapore"
    },

    // ssl: { // (optional)
    //   // Enables let's encrypt (optional)
    //   autogenerate: {
    //     email: 'email.address@domain.com',
    //     // comma separated list of domains
    //     domains: 'website.com,www.website.com'
    //   }
    // },

    docker: {
      // change to 'kadirahq/meteord' if your app is using Meteor 1.3 or older
      image: 'abernix/meteord:base'
    },

    // Show progress bar while uploading bundle to server
    // You might need to disable it on CI servers
    enableUploadProgressBar: true
  }

  // mongo: {
  //   version: '3.4.1',
  //   servers: {
  //     one: {}
  //   }
  // }
};
