import SimpleSchema from 'simpl-schema';

professors = new Meteor.Collection('professors');

professors.deny({
  insert: () => true,
  update: () => true,
  remove: () => true
})

const professorSchema = new SimpleSchema({
  universityId: {
    type: String
  },
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
  var Fiber = require('fibers')
  var fileReader = require('readline').createInterface({
    input: require('fs').createReadStream('assets/app/testdata.json')
  })
  fileReader.on('line', function (line) {
    var data = JSON.parse(line)
    Fiber(function () {
      console.log('Importing data for Prof. ' + data.name)
      var uid = universities.upsert({name: data.university}, {$set: {name: data.university, facultyIds: []}})
      if (!uid.insertedId) {
        uid = universities.findOne({name: data.university})._id
      } else {
        uid = uid.insertedId
      }
      var fid = faculties.upsert({name: data.faculty}, {$set: {name: data.faculty}})
      if (!fid.insertedId) {
        fid = faculties.findOne({name: data.faculty})._id
      } else {
        fid = fid.insertedId
      }
      data['facultyId'] = fid
      data['universityId'] = uid
      delete data.university
      delete data.faculty
      professors.insert(data)
    }).run()
  })
  setTimeout(function () {
    Fiber(function () {
      var p = professors.find({}).fetch()
      for (var i in p) {
        console.log(p[i].facultyId)
        universities.update({_id: p[i].universityId}, {$addToSet: {facultyIds: p[i].facultyId}})
      }
    }).run()
  }, 5000)
}
