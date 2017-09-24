import SimpleSchema from 'simpl-schema';

faculties = new Meteor.Collection('faculties');

faculties.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const facultySchema = new SimpleSchema({
  universityId: {
    type: String
  },
  name: {
    type: String
  }
})
