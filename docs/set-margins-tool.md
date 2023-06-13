---
title  : SetMargins+ tool
layout : default
---

A tool to set margins of glyphs with components without changing their internal relative positions.
{: .lead}

<div class='row'>

<div class='col-sm-4' markdown='1'>
![]({{ site.url }}/images/set-margins-tool.png){: .img-fluid}
</div>

<div class='col-sm-8' markdown='1'>
left mode
: Choose how the left value will be used. (see [Margin modes](#margin-modes))

left value
: New value for setting left margins.

right mode
: Choose how the right value will be used. (see [Margin modes](#margin-modes))

right value
: New value for setting right margins.

use beam
: Measure glyph margins using a horizontal beam.

beam
: Vertical position of the measuring beam.

left / right
: Select which margins to set.

apply
: Apply the new margins to the selected glyphs in the current font.

##### Margin modes
{: .mt-3 }

<table class='table-fluid'>
  <tr>
    <th width='25%'>mode</th>
    <th>description</th>
  </tr>
  <tr>
    <td><code>=</code></td>
    <td>set left margin equal to value</td>
  </tr>
  <tr>
    <td><code>+</code></td>
    <td>add/subtract value from left margin</td>
  </tr>
  <tr>
    <td><code>%</code></td>
    <td>multiply left margin by a percentage</td>
  </tr>
</table>
</div>

</div>

{% comment %}

<div class="card bg-light my-3">
<div class="card-header">note</div>
<div class="card-body" markdown='1'>
This dialog is a modified version of the [Set margins tool] in hTools3.
{: .card-text }
</div>
</div>

[Set margins tool]: http://hipertipo.gitlab.io/htools3-extension/glyphs/metrics/set-margins/

{% endcomment %}
