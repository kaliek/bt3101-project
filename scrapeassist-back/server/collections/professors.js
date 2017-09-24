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
  name: {
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
  promotionInstitution: {
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

professors.attachSchema(professorSchema)

if (!professors.find({}).count()) {
  var fileReader = require('readline').createInterface({
    input: require('fs').createReadStream('assets/app/testdata.json')
  })

  var Fiber = require('fibers')
  fileReader.on('line', function (line) {
    var data = JSON.parse(line)
    Fiber(function () {
      console.log('Importing data for Prof. ' + data.name)
      var uid = universities.findOne({name: data.university})
      if (!uid) {
        var uid = universities.insert({name: data.university})
      }
      var fid = faculties.findOne({name: data.faculty, universityId: uid})
      if (!fid) {
        var fid = faculties.insert({name: data.faculty, universityId: uid})
      }
      data['facultyId'] = fid
      delete data.university
      delete data.faculty
      professors.insert(data)
    }).run()
  })
}
