// Declare app level module which depends on filters, and services
angular.module('wcsc_app', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html', 
        controller: 'HomeController'})
      .otherwise({redirectTo: '/'});
  }]);
