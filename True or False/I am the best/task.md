<div class="step-text">
<h5 id="description">Description</h5>
<p>In this stage, we will continue working on the menu. Store the game score of each game.</p>
<h5 id="objectives">Objectives</h5>
<p>Let's break the task into several steps:</p>
<ul>
<li>Keep the functionality from the previous steps;</li>
<li>Save the player's score in the <em>scores.txt </em>file;</li>
<li>Use the format <code class="language-bash">User: hyper, Score: 20, Date: 2022-04-23</code> and add each new score line to the end of the score file;</li>
<li>Print out the menu and ask for an option;</li>
<li>If the option is <code class="language-bash">2</code>:
	<ul>
<li>If the score file is found:
		<ul>
<li>Print <code class="language-bash">Player scores</code> as the header;</li>
<li>Then print the scores to the standard output;</li>
</ul>
</li>
<li>If the file is not found or there are no scores inside:
		<ul>
<li>Print <code class="language-bash">File not found or no scores in it!</code>;</li>
</ul>
</li>
</ul>
</li>
<li>If the option is <code class="language-bash">3</code>:
	<ul>
<li>If the score file is found:
		<ul>
<li>Delete the <code class="language-bash">scores.txt</code>;</li>
<li>Display message <code class="language-bash">File deleted successfully!</code>;</li>
<li><code class="language-bash">scores.txt</code> should not exist after deletion;</li>
</ul>
</li>
<li>If the file is not found or there are no scores inside:
		<ul>
<li>Print <code class="language-bash">File not found or no scores in it!</code>;</li>
</ul>
</li>
</ul>
</li>
<li>If the option is <code class="language-bash">0</code>:
	<ul>
<li>Print <code class="language-bash">See you later!</code> and exit from the program</li>
</ul>
</li>
</ul>
<h5 id="examples">Examples</h5>
<p>The greater-than symbol followed by a space (<code class="language-bash">&gt; </code>) represents the user input. Note that it's not part of the input.</p>
<p><strong>Example 1</strong>:</p>
<pre><code class="language-bash">Welcome to the True or False Game!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 2
File not found or no scores in it!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 3
File not found or no scores in it!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 0
See you later!
</code></pre>
<p><strong>Example 2</strong>:</p>
<pre><code class="language-bash">Welcome to the True or False Game!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 1
What is your name?
&gt; hyper

Pong is the first commercially successful video game
True or False?
&gt; True
You are a genius!

The first mechanical computer - The Babbage Difference Engine - was designed by Charles Babbage in 1922
True or False?
&gt; False
Wonderful!

Rihanna is a rugby player
True or False?
&gt; False
Awesome!

Bright brothers had invented the first successful airplane
True or False?
&gt; False
You are a genius!

The heaviest land mammal is the African bush elephant
True or False?
&gt; False
Wrong answer, sorry!
hyper you have 4 correct answer(s).
Your score is 40 points.

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 1
What is your name?
&gt; jet

The International Space Station circles the globe every 900 minutes
True or False?
&gt; False
You are a genius!

The Sun is 109 times wider than Earth
True or False?
&gt; True
Wonderful!

John Bardeen - Walter Brattain - William Shockley invented the first working transistors at Bell Labs
True or False?
&gt; False
Wrong answer, sorry!
jet you have 2 correct answer(s).
Your score is 20 points.

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 0
See you later!
</code></pre>
<p><strong>Example 3</strong>:</p>
<pre><code class="language-bash">Welcome to the True or False Game!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 2
Player scores
User: hyper, Score: 40, Date: 2022-05-08
User: jet, Score: 20, Date: 2022-06-19

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 0
See you later!
</code></pre>
<p><strong>Example 4</strong>:</p>
<pre><code class="language-bash">Welcome to the True or False Game!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 3
File deleted successfully!

0. Exit
1. Play a game
2. Display scores
3. Reset scores
Enter an option:
&gt; 0
See you later!
</code></pre>
</div>