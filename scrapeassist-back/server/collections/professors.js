import SimpleSchema from 'simpl-schema';

professors = new Meteor.Collection('professors');

professors.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const professorSchema = new SimpleSchema({
  facultyId: {
    type: String
  },
  name : {
    type: String
  },
  rank: {
    type: String,
    optional: true
  },
  phdYear: {
    type: SimpleSchema.Integer,
    optional: true
  },
  phdInstitution: {
    type: String,
    optional: true
  },
  researchInterests: {
    type: String,
    optional: true
  },
  promotionYear: {
    type: SimpleSchema.Integer,
    optional: true
  },
  currentInstitution: {
    type: String,
    optional: true
  },
  relevantURLs: {
    type: Array,
    optional: true
  },
  'relevantURLs.$': {
    type: String
  }
})
