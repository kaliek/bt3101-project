module.exports = {
  servers: {
    one: {
      // TODO: set host address, username, and authentication method
      host: '115.66.242.122',
      username: 'root',
      //pem: '/home/theodore/.ssh/id_rsa',
      // or neither for authenticate from ssh-agent
    }
  },

  app: {
    // TODO: change app name and path
    name: 'scrapeassist-back',
    path: '../../scrapeassist-back',

    servers: {
      one: {},
    },

    buildOptions: {
      serverOnly: true,
    },

    env: {
      // TODO: Change to your app's url
      // If you are using ssl, it needs to start with https://
      ROOT_URL: 'http://app.com',
      MONGO_URL: 'mongodb://mongodb/',
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
      image: 'abernix/meteord:base',
	  args: [
		'--link=bt3101-mongo:mongodb',
	  ],
    },

    // Show progress bar while uploading bundle to server
    // You might need to disable it on CI servers
    enableUploadProgressBar: true
  }

  //mongo: {
  //  version: '3.4.1',
  //  servers: {
  //    one: {}
  //  }
  //}
};
