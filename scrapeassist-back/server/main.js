import { Meteor } from 'meteor/meteor';
import { Accounts } from 'meteor/accounts-base';

Meteor.startup(() => {
  if (!Meteor.users.find({"emails.address": 'admin@admin.com'}, {limit: 1}).count()>0) {
    Accounts.createUser({email: 'admin@admin.com', username: 'admin', password: 'admin'});
  }
});
