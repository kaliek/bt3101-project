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
  },
  facultyIds: {
    type: Array,
    defaultValue: []
  },
  'facultyIds.$': {
    type: String
  }
})

universities.attachSchema(universitySchema)

Meteor.publish({
  allUniversities: function () {
    return universities.find({})
  }
})
