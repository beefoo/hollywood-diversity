
// Classify app
var Classify = (function() {
  function Classify() {
    this.init();
  }

  Classify.prototype.init = function(){
    var _this = this;

    this.people = [];
    this.movies = [];
    this.roles = [];

    this.people_loaded = new $.Deferred();
    this.movies_loaded = new $.Deferred();
    this.roles_loaded = new $.Deferred();

    $.when(this.people_loaded, this.movies_loaded, this.roles_loaded).done(function() {
      _this.loadPerson();
    });

    this.loadListeners();
    this.loadTemplates();
    this.loadData();
  };

  Classify.prototype.loadData = function(){
    var _this = this;

    $.getJSON('/data/people.json', function(data) {
      _this.people = data;
      _this.people_loaded.resolve();
      console.log('Loaded '+_this.people.length+' people');
    });

    $.getJSON('/data/movies.json', function(data) {
      _this.movies = data;
      _this.movies_loaded.resolve();
      console.log('Loaded '+_this.movies.length+' movies');
    });

    $.getJSON('/data/roles.json', function(data) {
      _this.roles = data;
      _this.roles_loaded.resolve();
      console.log('Loaded '+_this.roles.length+' roles');
    });
  };

  Classify.prototype.loadListeners = function(){
    var _this = this;

    $('.gender-input').on('click', function(){
      var selected = $(this).hasClass('selected');
      $('.gender-input').removeClass('selected');
      if (!selected) $(this).addClass('selected');
    });

    $('.race-input').on('click', function(){
      $(this).toggleClass('selected');
      if ($(this).hasClass('unsure selected')) {
        $('.race-input:not(.unsure)').removeClass('selected');
      } else if (!$(this).hasClass('unsure')) {
        $('.race-input.unsure').removeClass('selected');
      }
    });

    $('.submit').on('click', function(){
      _this.submitClassification();
    });
  };

  Classify.prototype.loadingOn = function(){
    $('.info, .form').addClass('hide');
    $('.loading').removeClass('hide');
  };

  Classify.prototype.loadingOff = function(){
    $('.info, .form').removeClass('hide');
    $('.loading').addClass('hide');
  };

  Classify.prototype.loadPerson = function(){
    this.loadingOn();
    this.resetForm();

    // select a random person
    var person = _.sample(this.people);

    // pre-select gender/race
    if (person.gender) $('.gender-input[data-value="'+person.gender+'"]').addClass('selected')
    if (person.race) $('.race-input[data-value="'+person.race+'"]').addClass('selected')

    // retrieve roles and determine most frequent role
    person.roles = _.where(this.roles, {imdb_id: person.imdb_id});
    var roles = _.pluck(person.roles, 'role');
    var most_frequent_role = _.chain(roles).countBy().pairs().max(_.last).head().value();
    if (most_frequent_role=='cast') {
      most_frequent_role = 'actor';
      if (person.gender=='f') most_frequent_role = 'actress';
    }

    // generate urls
    person.google_image_url = 'https://www.google.com/search?q='+encodeURIComponent(person.name +' '+most_frequent_role)+'&tbm=isch';
    person.imdb_url = 'http://www.imdb.com/name/nm'+person.imdb_id+'/';
    person.wiki_url = 'https://en.wikipedia.org/wiki/'+person.name.replace(' ','_');
    person.google_url = 'https://www.google.com/search?q='+encodeURIComponent(person.name +' '+most_frequent_role);

    var rendered = Mustache.render(this.info_template, person);
    $('#info-container').html(rendered);

    this.loadingOff();
  };

  Classify.prototype.loadTemplates = function(){
    // load info template
    this.info_template = $('#info-template').html();
    Mustache.parse(this.info_template);
  };

  Classify.prototype.resetForm = function(){
    $('.input').removeClass('selected');
    $('textarea').val('');
  };

  Classify.prototype.submitClassification = function(){
    var data = {
      'user_id': '',
      'imdb_id': $('#imdb_id').val(),
      'gender': '',
      'races': [],
      'note': $('#note').val()
    };

    // retrieve gender
    if ($('.gender-input.selected').length) {
      data.gender = $('.gender-input.selected').first().attr('data-value');
    }

    // retrieve race
    if ($('.race-input.selected').length) {
      $('.race-input.selected').each(function(){
        data.races.push($(this).attr('data-value'));
      });
    }

    // save data
    console.log('Saving:', data);

    // load another person
    this.loadPerson();
  };

  return Classify;

})();

// Router
var router = Router({
  '/classify': function(){
    var app = new Classify();
  }
}).configure({html5history: true});

// Load router on ready
$(function() {
  router.init();
});
