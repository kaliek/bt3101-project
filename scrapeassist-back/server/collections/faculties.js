import SimpleSchema from 'simpl-schema';

faculties = new Meteor.Collection('faculties');

faculties.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const facultySchema = new SimpleSchema({
  name: {
    type: String
  }
})

faculties.attachSchema(facultySchema)

Meteor.publish({
  allFaculties: function () {
    return faculties.find({})
  }
})
