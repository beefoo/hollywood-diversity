<div class="classifications">
  <div class="form">
    <h2>What is this person's gender?</h2>

    <div class="button-group">
      <button data-value="f">Female</button>
      <button data-value="m">Male</button>
      <button data-value="o">Other</button>
    </div>

    <button class="unsure">I am unsure</button>

    <h2>What is this person's race?</h2>

    <p>Select all that apply. Hover over each button for more information.</p>

    <div class="button-group">
      <button data-value="w" title="A person having origins in any of the original peoples of Europe, the Middle East, or North Africa">White</button>
      <button data-value="b" title="A person having origins in any of the Black racial groups of Africa">Black</button>
      <button data-value="h" title="A person who identifies their origin as Hispanic, Latino, or Spanish.">Hispanic (Non-White)</button>
      <button data-value="a" title="A person having origins in any of the original peoples of the Far East, Southeast Asia, or the Indian subcontinent, or a person having origins in any of the original peoples of Hawaii, Guam, Samoa, or other Pacific Islands">Asian/Pacific Islander</button>
      <button data-value="o" title="A person having origins in any of the original peoples of North and South America and who maintains tribal affiliation or community attachment">American Indian or Alaska Native</button>
    </div>

    <button class="unsure">I am unsure</button>

    <h3>Add a note about this person's gender or race</h3>
    <textarea class="note"></textarea>

    <button class="submit">Submit</button>

  </div>
  <div class="info">
    <script id="info-template" type="x-tmpl-mustache">
    <h1>{{name}}</h1>
    <h3>Credits</h3>
    <ul>
      {{#roles}}
      <li>{{movie_name}} <em>({{role}})</em></li>
      {{/roles}}
    </ul>
    <div class="button-group">
      <button href="{{google_image_url}}">Do Google Image Search</button>
      <button href="{{imdb_url}}">Go To IMDb Page</button>
      <button href="{{wiki_url}}">Search on Wikipedia</button>
      <button href="{{google_url}}">Search on Google</button>
    </div>
    </script>
  </div>
</div>
