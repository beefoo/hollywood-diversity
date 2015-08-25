<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <title>Hollywood Diversity Classifier<?=(isset($title)&&$title)?' | '.$title:''?></title>
  <meta name="description" content="<?=(isset($description)&&$description)?$description.'. ':''?>An app for mapping actor/actress/director/writer/producer race and gender for 1000 major blockbuster movies from 1995-2014.">
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="/assets/css/app.css">
  <?= isset($css) ? $css : '' ?>

</head>
<body class="body-<?= $this->router->fetch_class() ?>-<?= $this->router->fetch_method() ?>">
