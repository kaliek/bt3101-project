import SimpleSchema from 'simpl-schema';

crawlrequests = new Meteor.Collection('crawlrequests');

crawlrequests.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
});

const crawlrequestSchema = new SimpleSchema({
  timeStampStart: {
    type: Date,
    autoValue: function() {
      if (!this.isUpdate) {
        return new Date();
      }
    }
  },
  timeStampEnd: {
    type: Date,
    optional: true
  },
  status: {
    type: Array,
    defaultValue: []
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
});

crawlrequests.attachSchema(crawlrequestSchema);

Meteor.methods({
  createCrawlRequest: function(fUrl, uId, fId) {
    crawlrequests.insert({facultyUrl: fUrl, universityId: uId, facultyId: fId})
  },
  createCrawlRequests: function(fUrls, uIds, fId) {
    if (fUrls.length !== uIds.length) {
      throw new Meteor.Error('Faculty URLs', 'All Faculty URLs must be filled')
    }
    for (i in fUrls) {
      crawlrequests.insert({facultyUrl: fUrls[i], universityId: uIds[i], facultyId: fId})
    }
  }
})

Meteor.publish({
  allCrawlRequests: function () {
    return crawlrequests.find({})
  }
})
