import SimpleSchema from 'simpl-schema';

crawlrequests = new Meteor.Collection('crawlrequests')

crawlrequests.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const crawlrequestSchema = new SimpleSchema({
  timeStamp: {
    type: Date,
    autoValue: function() {
      if (!this.isUpdate) {
        return new Date();
      }
    }
  },
  status: {
    type: Array
  },
  'status.$': {
    type: Boolean
  },
  facultyUrl: {
    type: String
  },
  universityId: {
    type: String
  },
  facultyId: {
    type: String
  },
  professorIds: {
    type: Array,
    defaultValue: []
  },
  'professorIds.$': {
    type: String
  }
})
