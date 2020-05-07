// clear descriptors on pageload (hotfix for back button bug)
$(window).bind("pageshow", function() {
   $('#descriptors-input').val('');
});

// flag for initial click on descriptors
var descriptors_clicked = false;

$(function () {
   $('#descriptors-input_tag').tooltip({'placement': 'right', 'trigger':'focus', 'title': 'Start typing and select any number of descriptors from the dropdown'});
   $('[data-toggle="tooltip"]').tooltip();
})

const descriptors_all = {{descriptors|tojson}};
const descriptors_initial = descriptors_all.slice(0, 50);
$('.tagsinput').tagsInput({
   'width': '100%',
   'placeholder': 'eg. "light bodied, luminous, lush"',
   'autocomplete': {
      source: descriptors_initial,
      delay: 0,
      minLength: 0
   },
   'values': descriptors_all
});
$('#descriptors-input_tag').focus(function(){     
   $(this).data("uiAutocomplete").search($(this).val());
   if (!descriptors_clicked) {
      $('#descriptors-input_tag').autocomplete({
         source: descriptors_all,
         delay: 0,
         minLength: 0
      });
      descriptors_clicked = true;
   }
});

function checkCocktail(select) {
   if (select.value == 'cocktail') {
      document.getElementById('base-line').style.display = 'flex';
      document.getElementById('price-line').style.display = 'none';
      document.getElementById('abv-line').style.display = 'none';
   } else {
      document.getElementById('base-line').style.display = 'none';
      document.getElementById('price-line').style.display = 'flex';
      document.getElementById('abv-line').style.display = 'flex';
   }
}

$(function() {
   var availableTags = ['vodka', 'Midori', 'sloe', 'lychee', 'Chambord', 'Averna', 'beer', 'Campari', 'coffee', 'banana', 'sherry', 'Champagne', 'Mekhong', 'Jagermeister', 'Irish', 'Pimm', 'sake', 'nonalcoholic', 'RumChata', 'peach', 'absinthe', 'rum', 'Galliano', 'Southern', 'melon', 'Benedictine', 'brandy', 'tequila', 'pisco', 'shooter', 'chocolate', 'gin', 'Cointreau', 'whiskey', 'cachaca', 'Strega', 'vermouth', 'wine', 'cachaça', 'Frangelico', 'Grand', 'TyKu', 'Agavero'];
   $('#base-input').autocomplete({
      source: availableTags,
      delay: 0,
      minLength: 0
   }).focus(function(){            
      $(this).data("uiAutocomplete").search($(this).val());
   });
});

$(function() {
   $('.main-form').submit(function() {
      $(this).find(':input').filter(function(){ return !this.value; }).attr('disabled', 'disabled');
      return true; // ensure form still submits
   });
});

// input masks
$(function() {
   // price inputs
   $('#minprice-input').inputmask('currency', {
      prefix: '$',
      showMaskOnHover: false,
      rightAlign: false,
      clearMaskOnLostFocus: true,
      clearIncomplete: true,
   });
   $('#minprice-input').blur(function() {
      if ($('#minprice-input').val() == '$0.00') {
         $('#minprice-input').val('');
      }
   });
   $('#maxprice-input').inputmask('currency', {
      prefix: "$",
      showMaskOnHover: false,
      rightAlign: false,
      clearMaskOnLostFocus: true,
      clearIncomplete: true,
   });
   $('#maxprice-input').blur(function() {
      if ($('#maxprice-input').val() == '$0.00') {
         $('#maxprice-input').val('');
      }
   });

   // abv inputs
   $('#minabv-input').inputmask('percentage', {
      showMaskOnHover: false,
      rightAlign: false,
      clearMaskOnLostFocus: true,
      clearIncomplete: true,
   });
   $('#maxabv-input').inputmask('percentage', {
      showMaskOnHover: false,
      rightAlign: false,
      clearMaskOnLostFocus: true,
      clearIncomplete: true,
   });
});