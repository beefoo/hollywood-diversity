<div class="classifications container">

  <div class="info col half hide">
    <div id="info-container"></div>
    <script id="info-template" type="x-tmpl-mustache">
    <h1>{{name}}</h1>
    <div class="image">
      {{#img}}<img src="{{{img}}}" />{{/img}}
      {{^img}}<p>(No image available)</p>{{/img}}
    </div>
    <div class="button-group">
      <a class="button" href="{{google_image_url}}" target="_blank">Do Google Image Search</a>
      <a class="button" href="{{imdb_url}}" target="_blank">Go To IMDb Page</a>
      <a class="button" href="{{wiki_url}}" target="_blank">Search on Wikipedia</a>
      <a class="button" href="{{google_url}}" target="_blank">Search on Google</a>
    </div>
    <h3>Credits</h3>
    <ul>
      {{#roles}}
      <li>{{movie_name}} <em>({{role}})</em></li>
      {{/roles}}
    </ul>
    <input id="imdb_id" type="hidden" value="{{imdb_id}}" />
    </script>
  </div>

  <div class="form col half hide">
    <h2>What is this person's gender?</h2>

    <div class="button-group">
      <button data-value="f" class="input gender-input">Female</button>
      <button data-value="m" class="input gender-input">Male</button>
      <button data-value="o" class="input gender-input">Other</button>
    </div>

    <button data-value="u" class="input gender-input unsure">I am unsure</button>

    <h2>What is this person's race?</h2>

    <p>Select all that apply. Hover over each button for more information.</p>

    <div class="button-group">
      <button data-value="w" class="input race-input" title="A person having origins in any of the original peoples of Europe, the Middle East, or North Africa">White</button>
      <button data-value="b" class="input race-input" title="A person having origins in any of the Black racial groups of Africa">Black</button>
      <button data-value="h" class="input race-input" title="A person who identifies their origin as Hispanic, Latino, or Spanish.">Hispanic (Non-White)</button>
      <button data-value="a" class="input race-input" title="A person having origins in any of the original peoples of the Far East, Southeast Asia, or the Indian subcontinent, or a person having origins in any of the original peoples of Hawaii, Guam, Samoa, or other Pacific Islands">Asian/Pacific Islander</button>
      <button data-value="o" class="input race-input" title="A person having origins in any of the original peoples of North and South America and who maintains tribal affiliation or community attachment">American Indian</button>
    </div>

    <button data-value="u" class="input race-input unsure">I am unsure</button>
    <h4>Add a note about this person</h4>
    <textarea id="note"></textarea>

    <input id="user_id" type="hidden" value="<?= $user_id ?>" />
    <button class="submit">Submit</button>

  </div>

  <div class="loading">Loading data. One moment please...</div>

</div>
