use strict;
use warnings;
use Prima qw(Application);
$\ = "\n";

sub chaikin{
	my (@points) = @_;
	my @new_points;
	for (my $i = 0; $i <= $#points; $i+=2){
		if ($points[$i+3]){
			push (@new_points, ($points[$i]*3+$points[$i+2]*1)/4); #x1
			push (@new_points, ($points[$i+1]*3+$points[$i+3]*1)/4); #y1
			push (@new_points, ($points[$i]*1+$points[$i+2]*3)/4); #x2
			push (@new_points, ($points[$i+1]*1+$points[$i+3]*3)/4); #y2
		}
	}
	
	return @new_points;
}

my @initial_points = qw(10 10 20 100 80 20 150 190);

my @final_points = @initial_points;
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
 @final_points = chaikin(@final_points);
#print join(",",@final_points);

#### MAKE THE IMAGE
   my $i = Prima::Image-> new(
      width => 200,
      height => 200,
      #type   => im::BW, # same as im::bpp1 | im::GrayScale
   );

   # draw something
   $i-> begin_paint; 
   $i-> color( cl::White);
   #$i->line(2,2,50,50);
   #$i->line(50,50,150,50);
   #$i->lines(\@final_points);
   for (my $j = 0; $j<= $#final_points; $j+=2){
		if ($final_points[$j+3]){
			$i->line( int $final_points[$j], int $final_points[$j+1], int $final_points[$j+2], int $final_points[$j+3] );
			print $final_points[$j].' '.$final_points[$j+1]." ".$final_points[$j+2].' '.$final_points[$j+3];
		}
   }
   $i-> end_paint; 

   # mangle
   #$i-> size( 64, 64);

   # file operations
   $i-> save('test.jpg') or die "Error saving:$@\n";
