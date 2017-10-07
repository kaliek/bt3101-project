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

Meteor.publish({
  allUniversities: function () {
    return universities.find({})
  }
})

Meteor.methods({
  createUniversities: function(names) {
    var Ids = []
    for (var i in names) {
      Ids.push(universities.insert({name: names[i]}))
    }
    return Ids
  }
})
