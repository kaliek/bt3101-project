import SimpleSchema from 'simpl-schema';

universities = new Meteor.Collection('universities')

universities.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const universitySchema = new SimpleSchema({
  name: {
    type: String
  }
})

universities.attachSchema(universitySchema)
